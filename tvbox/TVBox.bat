@echo off
setlocal EnableDelayedExpansion
title Optimizador de TV Box
cd /d "%~dp0"

set "ADB=%~dp0platform-tools\adb.exe"
set "PUERTO=5555"

rem ---------- 1. Descargar ADB (solo la primera vez) ----------
if exist "%ADB%" goto pedir_ip
echo.
echo Descargando las herramientas oficiales de Android (ADB) desde Google...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile 'platform-tools.zip'; Expand-Archive -Path 'platform-tools.zip' -DestinationPath '.' -Force; Remove-Item 'platform-tools.zip'"
if exist "%ADB%" goto pedir_ip
echo.
echo No se pudo descargar ADB. Revisa que la PC tenga internet y volve a abrir este archivo.
pause
exit /b 1

rem ---------- 2. IP del TV Box ----------
:pedir_ip
set "IP="
if exist "ip.txt" set /p IP=<"ip.txt"
if not defined IP goto escribir_ip
echo.
echo IP guardada del TV Box: %IP%
set "NUEVA="
set /p NUEVA="Apreta Enter para usarla, o escribi otra IP: "
if defined NUEVA set "IP=%NUEVA%"
goto guardar_ip

:escribir_ip
echo.
echo La IP del TV Box esta en: Ajustes ^> Informacion ^> Estado  (o en Ajustes ^> Red)
set /p IP="Escribi la IP del TV Box (ejemplo 192.168.0.25): "
if not defined IP goto escribir_ip

:guardar_ip
>"ip.txt" echo %IP%
set "DEV=%IP%:%PUERTO%"
set ADBS="%ADB%" -s %DEV% shell

rem ---------- 3. Conectar ----------
:conectar
echo.
echo Conectando con %DEV% ...
echo (Si en la TV aparece "Permitir depuracion?", marca "Permitir siempre" y Aceptar)
"%ADB%" connect %DEV% >nul 2>&1
"%ADB%" -s %DEV% get-state > "%TEMP%\tvbox_estado.txt" 2>&1
findstr /b /c:"device" "%TEMP%\tvbox_estado.txt" >nul
if not errorlevel 1 goto menu

echo.
echo No se pudo conectar. Revisa:
echo   1. Que la PC y el TV Box esten en el MISMO router (por wifi o por cable).
echo   2. En el TV Box: Ajustes ^> Informacion ^> toca 7 veces "Compilacion".
echo      Despues entra a "Opciones de desarrollador" y activa "Depuracion USB"
echo      y "Depuracion por red / ADB por red" si aparece.
echo   3. Mira la TV: si pide permiso, marca "Permitir siempre" y Aceptar.
echo.
set "R="
set /p R="Enter para reintentar, o escribi N para cambiar la IP: "
"%ADB%" disconnect %DEV% >nul 2>&1
if /i "%R%"=="N" goto escribir_ip
goto conectar

rem ---------- 4. Menu ----------
:menu
cls
echo ==========================================================
echo    OPTIMIZADOR DE TV BOX      conectado a %DEV%
echo ==========================================================
echo   1. Revisar el equipo  (crea reporte.txt)
echo   2. Optimizar          (mas rapido, todo reversible)
echo   3. Instalar las apps que pusiste en la carpeta "apks"
echo   4. Ver las apps instaladas
echo   5. Desactivar una app puntual
echo   6. Restaurar todo como estaba
echo   7. Reiniciar el TV Box
echo   8. Respaldar la app Point en la PC  (carpeta "respaldo")
echo   0. Salir
echo.
set "OP="
set /p OP="Elegi una opcion y apreta Enter: "
if "%OP%"=="1" goto revisar
if "%OP%"=="2" goto optimizar
if "%OP%"=="3" goto instalar
if "%OP%"=="4" goto ver_apps
if "%OP%"=="5" goto puntual
if "%OP%"=="6" goto restaurar
if "%OP%"=="7" goto reiniciar
if "%OP%"=="8" goto respaldo_menu
if "%OP%"=="0" goto salir
goto menu

:revisar
echo.
echo Generando reporte, espera unos segundos...
> reporte.txt (
  echo ===== EQUIPO =====
  %ADBS% getprop ro.product.manufacturer
  %ADBS% getprop ro.product.model
  %ADBS% getprop ro.board.platform
  echo ----- Android real / compilacion / parche -----
  %ADBS% getprop ro.build.version.release
  %ADBS% getprop ro.build.display.id
  %ADBS% getprop ro.build.version.security_patch
  %ADBS% getprop ro.build.type
  echo.
  echo ===== MEMORIA =====
  %ADBS% "head -n 3 /proc/meminfo"
  echo.
  echo ===== ESPACIO =====
  %ADBS% "df -h /data"
  echo.
  echo ===== LO QUE MAS CONSUME AHORA =====
  %ADBS% "top -b -n 1 -m 15"
  echo.
  echo ===== APPS INSTALADAS POR EL USUARIO / FABRICANTE ^(installer=null = sin tienda^) =====
  %ADBS% pm list packages -3 -i
  echo.
  echo ===== APPS DEL SISTEMA =====
  %ADBS% pm list packages -s
  echo.
  echo ===== APPS DESACTIVADAS =====
  %ADBS% pm list packages -d
)
echo.
echo Listo. Se creo el archivo reporte.txt en esta carpeta.
echo Pasaselo a Claude para que te diga que mas se puede sacar.
start "" notepad reporte.txt
pause
goto menu

:optimizar
echo.
echo [0/5] Respaldo de seguridad de las apps protegidas (Point)...
call :respaldo
echo [1/5] Animaciones al doble de rapido...
%ADBS% settings put global window_animation_scale 0.5
%ADBS% settings put global transition_animation_scale 0.5
%ADBS% settings put global animator_duration_scale 0.5
echo [2/5] Apagando el protector de pantalla (consume recursos)...
%ADBS% settings put secure screensaver_enabled 0
echo [3/5] Liberando cache de todas las apps...
%ADBS% pm trim-caches 999G
echo [4/5] Desactivando apps innecesarias de la lista "desactivar.txt"...
for /f "usebackq eol=# tokens=1" %%p in ("desactivar.txt") do call :desactivar %%p
echo [5/5] Cerrando apps en segundo plano...
%ADBS% am kill-all
echo.
echo Optimizacion terminada. Conviene reiniciar el TV Box (opcion 7).
pause
goto menu

:desactivar
rem Nunca tocar las apps protegidas (proteger.txt, ej. Point)
echo %1| findstr /i /l /g:"proteger.txt" >nul
if not errorlevel 1 (
  echo   PROTEGIDA, no se toca: %1
  goto :eof
)
%ADBS% pm path %1 2>nul | findstr /b "package:" >nul
if errorlevel 1 (
  echo   ^(no esta instalada^) %1
  goto :eof
)
%ADBS% pm disable-user --user 0 %1 2>nul | findstr /c:"disabled" >nul
if errorlevel 1 (
  echo   No se pudo desactivar: %1
  goto :eof
)
>>desactivadas.log echo %1
echo   Desactivada: %1
goto :eof

:respaldo_menu
call :respaldo
pause
goto menu

:respaldo
if not exist "respaldo" mkdir "respaldo"
%ADBS% pm list packages > "%TEMP%\tvbox_pk.txt"
findstr /i /l /g:"proteger.txt" "%TEMP%\tvbox_pk.txt" > "%TEMP%\tvbox_prot.txt"
set "HAY="
for /f "usebackq tokens=2 delims=:" %%p in ("%TEMP%\tvbox_prot.txt") do (
  set "HAY=1"
  call :respaldar_pkg %%p
)
if not defined HAY echo   No encontre ninguna app con "point" en el nombre. Pasale reporte.txt a Claude.
goto :eof

:respaldar_pkg
if not exist "respaldo\%1" mkdir "respaldo\%1"
%ADBS% pm path %1 > "%TEMP%\tvbox_path.txt"
for /f "usebackq tokens=2 delims=:" %%a in ("%TEMP%\tvbox_path.txt") do "%ADB%" -s %DEV% pull %%a "respaldo\%1" >nul
echo   Respaldada: %1  ^(carpeta respaldo\%1^)
goto :eof

:instalar
echo.
if not exist "apks\*.apk" (
  echo No hay archivos .apk en la carpeta "apks".
  echo Descarga ahi los APK ^(SmartTube, TV Bro, etc. - ver LEEME.md^) y volve a elegir esta opcion.
  pause
  goto menu
)
for %%f in ("apks\*.apk") do (
  echo Instalando %%~nxf ...
  "%ADB%" -s %DEV% install -r "%%f"
)
echo.
echo Instalacion terminada.
pause
goto menu

:ver_apps
echo.
echo Apps instaladas (no del sistema):
%ADBS% pm list packages -3
echo.
pause
goto menu

:puntual
echo.
echo Tip: el nombre lo sacas de la opcion 4 (lo que va despues de "package:").
set "PKG="
set /p PKG="Nombre del paquete (ejemplo com.ejemplo.app), o Enter para volver: "
if not defined PKG goto menu
call :desactivar %PKG%
pause
goto menu

:restaurar
echo.
echo Volviendo animaciones y protector de pantalla a lo normal...
%ADBS% settings put global window_animation_scale 1.0
%ADBS% settings put global transition_animation_scale 1.0
%ADBS% settings put global animator_duration_scale 1.0
%ADBS% settings put secure screensaver_enabled 1
if not exist desactivadas.log goto restaurar_fin
for /f "usebackq" %%p in ("desactivadas.log") do (
  echo   Reactivando %%p
  %ADBS% pm enable %%p >nul 2>&1
)
del desactivadas.log
:restaurar_fin
echo.
echo Todo restaurado.
pause
goto menu

:reiniciar
"%ADB%" -s %DEV% reboot
echo El TV Box se esta reiniciando.
pause
goto salir

:salir
"%ADB%" disconnect %DEV% >nul 2>&1
endlocal
exit /b 0
