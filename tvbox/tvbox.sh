#!/usr/bin/env bash
# Optimizador de TV Box - version Mac / Linux. Mismas opciones que TVBox.bat.
cd "$(dirname "$0")" || exit 1
PUERTO=5555

if ! command -v adb >/dev/null 2>&1 && [ ! -x platform-tools/adb ]; then
  echo "Descargando las herramientas oficiales de Android (ADB) desde Google..."
  case "$(uname)" in Darwin) SO=darwin ;; *) SO=linux ;; esac
  curl -fsSL -o pt.zip "https://dl.google.com/android/repository/platform-tools-latest-$SO.zip" \
    && unzip -oq pt.zip && rm -f pt.zip
fi
ADB=adb; [ -x platform-tools/adb ] && ADB=./platform-tools/adb

IP=$(cat ip.txt 2>/dev/null)
read -r -p "IP del TV Box [${IP:-ej. 192.168.0.25}]: " NUEVA
IP=${NUEVA:-$IP}
[ -z "$IP" ] && { echo "Falta la IP."; exit 1; }
echo "$IP" > ip.txt
DEV="$IP:$PUERTO"
sh_() { "$ADB" -s "$DEV" shell "$@"; }

while true; do
  echo "Conectando con $DEV (si la TV pide permiso: 'Permitir siempre')..."
  "$ADB" connect "$DEV" >/dev/null 2>&1
  [ "$("$ADB" -s "$DEV" get-state 2>/dev/null)" = "device" ] && break
  echo "No se pudo conectar. Revisa: mismo router, 'Depuracion USB/por red' activada, y acepta el aviso en la TV."
  read -r -p "Enter para reintentar (Ctrl+C para salir) " _
  "$ADB" disconnect "$DEV" >/dev/null 2>&1
done

desactivar() {
  sh_ pm path "$1" 2>/dev/null | grep -q '^package:' || { echo "  (no esta instalada) $1"; return; }
  if sh_ pm disable-user --user 0 "$1" 2>/dev/null | grep -q disabled; then
    echo "$1" >> desactivadas.log; echo "  Desactivada: $1"
  else echo "  No se pudo desactivar: $1"; fi
}

while true; do
  cat <<EOF

==========  OPTIMIZADOR DE TV BOX  ($DEV)  ==========
 1. Revisar el equipo (crea reporte.txt)
 2. Optimizar (mas rapido, todo reversible)
 3. Instalar las apps de la carpeta "apks"
 4. Ver las apps instaladas
 5. Desactivar una app puntual
 6. Restaurar todo como estaba
 7. Reiniciar el TV Box
 0. Salir
EOF
  read -r -p "Opcion: " OP
  case "$OP" in
    1) {
         echo "===== EQUIPO ====="
         for p in ro.product.manufacturer ro.product.model ro.board.platform ro.build.version.release \
                  ro.build.display.id ro.build.version.security_patch ro.build.type; do
           echo "$p = $(sh_ getprop $p)"; done
         echo; echo "===== MEMORIA ====="; sh_ "head -n 3 /proc/meminfo"
         echo; echo "===== ESPACIO ====="; sh_ "df -h /data"
         echo; echo "===== LO QUE MAS CONSUME ====="; sh_ "top -b -n 1 -m 15"
         echo; echo "===== APPS DE USUARIO/FABRICANTE (installer=null = sin tienda) ====="; sh_ pm list packages -3 -i
         echo; echo "===== APPS DEL SISTEMA ====="; sh_ pm list packages -s
         echo; echo "===== APPS DESACTIVADAS ====="; sh_ pm list packages -d
       } > reporte.txt 2>&1
       echo "Listo: reporte.txt (pasaselo a Claude)." ;;
    2) for k in window_animation_scale transition_animation_scale animator_duration_scale; do
         sh_ settings put global $k 0.5; done
       sh_ settings put secure screensaver_enabled 0
       sh_ pm trim-caches 999G
       grep -v '^\s*#' desactivar.txt | awk 'NF{print $1}' | while read -r p; do desactivar "$p"; done
       sh_ am kill-all
       echo "Optimizacion terminada. Conviene reiniciar (opcion 7)." ;;
    3) shopt -s nullglob; apks=(apks/*.apk)
       [ ${#apks[@]} -eq 0 ] && echo "No hay .apk en la carpeta apks (ver LEEME.md)."
       for f in "${apks[@]}"; do echo "Instalando $f"; "$ADB" -s "$DEV" install -r "$f"; done ;;
    4) sh_ pm list packages -3 ;;
    5) read -r -p "Nombre del paquete: " PKG; [ -n "$PKG" ] && desactivar "$PKG" ;;
    6) for k in window_animation_scale transition_animation_scale animator_duration_scale; do
         sh_ settings put global $k 1.0; done
       sh_ settings put secure screensaver_enabled 1
       if [ -f desactivadas.log ]; then
         sort -u desactivadas.log | while read -r p; do echo "  Reactivando $p"; sh_ pm enable "$p" >/dev/null 2>&1; done
         rm -f desactivadas.log
       fi
       echo "Todo restaurado." ;;
    7) "$ADB" -s "$DEV" reboot; echo "Reiniciando."; exit 0 ;;
    0) "$ADB" disconnect "$DEV" >/dev/null 2>&1; exit 0 ;;
  esac
done
