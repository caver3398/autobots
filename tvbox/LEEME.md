# Optimizador de TV Box

Kit para limpiar, acelerar y mejorar el TV Box (modelo **R3**, en realidad Android 10 aunque diga "14.0").
Todo lo que hace es **reversible**: nada se borra, solo se desactiva.

---

## ¿Qué necesito?

| Tengo... | ¿Sirve? |
|---|---|
| PC con Windows, Mac o Linux conectada al **mismo router** que el TV Box (por Wi‑Fi **o por cable**) | ✅ Sí: usá el kit automático |
| PC sin Wi‑Fi y sin cable al router | ❌ No. Conectala con un cable de red al router y listo |
| Solo un **iPhone** | ⚠️ Solo la guía manual (más abajo). No hay app confiable de ADB para iPhone |
| Un celular **Android** en el mismo Wi‑Fi | ✅ Con la app *Bugjaeger* o *Remote ADB Shell* se pueden escribir los mismos comandos a mano |

---

## Paso 1: preparar el TV Box (una sola vez)

1. **Ajustes → Información** → tocá **7 veces** la opción **Compilación** hasta que diga "Ya sos desarrollador".
2. Volvé atrás → entrá a **Opciones de desarrollador** → activá **Depuración USB** y, si aparece, **Depuración por red / ADB por red**.
3. Anotá la **IP** del TV Box: **Ajustes → Información → Estado** (algo como `192.168.0.25`).

## Paso 2: usar el kit en la PC

1. Bajá la carpeta `tvbox` a la PC.
2. **Windows:** doble clic en **`TVBox.bat`**.
   **Mac/Linux:** abrí la Terminal en la carpeta y ejecutá `bash tvbox.sh`.
3. La primera vez descarga solo las herramientas oficiales de Google (ADB).
4. Escribí la IP. **Mirá la TV**: si aparece "¿Permitir depuración?", marcá **Permitir siempre** → **Aceptar**.
5. Usá el menú en este orden:
   - **1. Revisar**: crea `reporte.txt` con el estado real del equipo y todas sus apps. **Pasáselo a Claude** para que te diga qué más se puede sacar y si hay algo sospechoso.
   - **2. Optimizar**: animaciones al doble de rápido, apaga el protector de pantalla, limpia la caché, desactiva las apps de `desactivar.txt` y cierra lo que corre de fondo.
   - **3. Instalar apps**: instala los `.apk` que pongas en la carpeta `apks`.
   - **7. Reiniciar**.
   - Si algo no te gusta: **6. Restaurar** vuelve todo como estaba.

## Paso 3: apps recomendadas

Descargá los `.apk` en la carpeta `apks` y usá la opción 3, o instalalos desde la Play Store de la TV.

| Para qué | App | Dónde |
|---|---|---|
| **Buscador / navegador web** cómodo con el control | **TV Bro** | github.com/truefedex/tv-bro/releases |
| YouTube más rápido y sin publicidad | **SmartTube** | github.com/yuliskov/SmartTube/releases (versión *stable*) |
| Pantalla de inicio moderna y liviana | **Projectivy Launcher** | Play Store de la TV |
| Revisar si trae virus de fábrica | **Malwarebytes** | Play Store |

> Bajá los APK **solo** de esas páginas oficiales. Las páginas de "APK gratis" suelen traer malware.

---

## Guía manual (si solo tenés el iPhone)

Desde el control remoto, en el TV Box:

1. **Animaciones**: Opciones de desarrollador → *Escala de animación de ventana*, *de transición* y *duración de animador* → **0.5x**.
2. **Limpieza**: Ajustes → Apps → desinstalá lo que no uses. En YouTube, Netflix y Play Store: **Borrar caché**.
3. **Protector de pantalla**: Ajustes → Preferencias → Protector de pantalla → **Desactivado**.
4. **Navegador**: Play Store → buscá **TV Bro** (o "Downloader" y desde ahí descargá TV Bro y SmartTube).
5. **Launcher**: Play Store → **Projectivy Launcher** → elegilo como pantalla de inicio.
6. **Seguridad**: instalá **Malwarebytes** y hacé un escaneo.
7. Reiniciá el TV Box.

---

## ⚠️ Importante sobre este equipo

- **La app Point está protegida**: el kit nunca la desactiva (lista `proteger.txt`) y antes de optimizar guarda una copia del instalador en la carpeta `respaldo` de tu PC.
- Dice "Android 14" pero es **Android 10** con firmware de prueba (`userdebug / test-keys`) y su último parche de seguridad es de **diciembre de 2019**.
- Equipos así a veces vienen con malware de fábrica. **No inicies sesión con tu cuenta principal de Google** ni lo uses para bancos o compras.
- Para una mejora de verdad: un **Chromecast con Google TV / Google TV Streamer / Fire TV Stick** es mucho más rápido y seguro.
