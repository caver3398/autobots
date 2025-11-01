# 📥 Guía de Descarga de Videos F1

## 🎯 Descripción

Sistema completo para descargar videos de Formula 1 generados, con o sin música, directamente desde tu navegador.

## 🚀 Inicio Rápido

### 1. Generar el Video Base

```bash
npm run generate-video
```

Esto creará: `output/f1_racing_video.mp4` (2.3 MB aprox.)

### 2. (Opcional) Agregar Música

```bash
npm run add-music /ruta/a/tu/musica.mp3
```

Esto creará: `output/f1_racing_video_with_music.mp4`

### 3. Iniciar el Servidor

```bash
npm start
```

El servidor se iniciará en: `http://localhost:3000`

### 4. Acceder a la Página de Descarga

Abre tu navegador y visita:

```
http://localhost:3000/download
```

## 📋 Rutas Disponibles

### 🌐 Interfaz Web

| Ruta | Descripción |
|------|-------------|
| `/download` | Página principal con botones de descarga |

### ⬇️ Descarga Directa

| Ruta | Descripción | Archivo |
|------|-------------|---------|
| `/download/video` | Descarga video sin música | `f1_racing_video.mp4` |
| `/download/video-with-music` | Descarga video con música | `f1_racing_video_with_music.mp4` |

### ▶️ Streaming (Ver en Navegador)

| Ruta | Descripción |
|------|-------------|
| `/download/stream/video` | Reproduce video sin música |
| `/download/stream/video-with-music` | Reproduce video con música |

## 💻 Uso desde Línea de Comandos

### Descargar con curl

```bash
# Video sin música
curl -O http://localhost:3000/download/video

# Video con música
curl -O http://localhost:3000/download/video-with-music
```

### Descargar con wget

```bash
# Video sin música
wget http://localhost:3000/download/video

# Video con música
wget http://localhost:3000/download/video-with-music
```

## 🔧 Características Técnicas

### Video Sin Música
- **Formato:** MP4 (H.264)
- **Resolución:** 1080x1920 (vertical)
- **FPS:** 60
- **Duración:** 15 segundos
- **Tamaño:** ~2.3 MB
- **Calidad:** Alta (CRF 18)

### Video Con Música
- **Todo lo anterior +**
- **Audio:** AAC 192kbps
- **Tamaño:** Variable (depende de la música)

## 📱 Uso en Redes Sociales

### Instagram Reels
1. Descarga el video con música
2. Abre Instagram → Crear → Reel
3. Sube el video descargado
4. Agrega hashtags: `#F1 #Formula1 #Racing`
5. ¡Publica!

### TikTok
1. Descarga el video
2. Abre TikTok → Crear → Subir
3. Selecciona el video
4. Edita y publica

### YouTube Shorts
1. Descarga el video
2. YouTube Studio → Crear → Subir videos
3. Selecciona el video
4. Marca como "Short"
5. Publica

## 🎵 Agregar Música

### Fuentes de Música Sin Copyright

- **YouTube Audio Library:** https://studio.youtube.com/
- **Epidemic Sound:** https://www.epidemicsound.com/
- **Free Music Archive:** https://freemusicarchive.org/
- **Incompetech:** https://incompetech.com/

### Formatos Soportados

- MP3
- WAV
- AAC
- M4A
- OGG

### Ejemplo

```bash
# Descargar música de ejemplo (dominio público)
wget https://example.com/racing-music.mp3

# Agregar al video
npm run add-music racing-music.mp3
```

## 🧪 Verificar Estado

Ejecuta el script de prueba para ver qué videos están disponibles:

```bash
node test-download.js
```

Salida esperada:
```
🧪 PRUEBA DE RUTAS DE DESCARGA
==================================================

📁 Verificando archivos...

✅ Video sin música: DISPONIBLE
   Ruta: /vercel/sandbox/output/f1_racing_video.mp4
   Tamaño: 2.25 MB
   URL descarga: http://localhost:3000/download/video
   URL streaming: http://localhost:3000/download/stream/video

✅ Video con música: DISPONIBLE
   Ruta: /vercel/sandbox/output/f1_racing_video_with_music.mp4
   Tamaño: 3.45 MB
   URL descarga: http://localhost:3000/download/video-with-music
   URL streaming: http://localhost:3000/download/stream/video-with-music
```

## 🔒 Seguridad

- Los videos solo se sirven desde el directorio `output/`
- Validación de existencia de archivos antes de servir
- Headers de seguridad configurados
- No se permite acceso a otros directorios

## 🐛 Solución de Problemas

### Error: "Video no encontrado"

**Causa:** El video no ha sido generado.

**Solución:**
```bash
npm run generate-video
```

### Error: "Video con música no encontrado"

**Causa:** No se ha agregado música al video.

**Solución:**
```bash
npm run add-music /ruta/a/musica.mp3
```

### Error: "Cannot GET /download"

**Causa:** El servidor no está corriendo.

**Solución:**
```bash
npm start
```

### El video no se descarga, se reproduce

**Causa:** El navegador está configurado para reproducir MP4.

**Solución:** Usa las rutas de descarga directa o haz clic derecho → "Guardar como"

## 📊 Estructura de Archivos

```
/vercel/sandbox/
├── output/
│   ├── f1_racing_video.mp4              # Video sin música
│   └── f1_racing_video_with_music.mp4   # Video con música
├── routes/
│   └── download.js                       # Rutas de descarga
├── views/
│   └── download.pug                      # Interfaz web
├── generate-f1-video.js                  # Generador de video
├── add-music.js                          # Agregar música
└── test-download.js                      # Script de prueba
```

## 🎨 Personalización

### Cambiar Nombre de Archivo de Descarga

Edita `routes/download.js`:

```javascript
res.setHeader('Content-Disposition', 'attachment; filename="mi_video_f1.mp4"');
```

### Agregar Más Formatos

Puedes agregar rutas para otros formatos (WebM, AVI, etc.) siguiendo el mismo patrón.

## 📞 Soporte

Si encuentras problemas:

1. Verifica que Node.js esté instalado: `node --version`
2. Verifica que las dependencias estén instaladas: `npm install`
3. Ejecuta el script de prueba: `node test-download.js`
4. Revisa los logs del servidor

## 🎉 ¡Listo!

Ahora puedes:
- ✅ Generar videos de F1 de alta calidad
- ✅ Agregar música personalizada
- ✅ Descargar directamente desde el navegador
- ✅ Ver videos en streaming
- ✅ Compartir en redes sociales

---

**¡Disfruta creando contenido viral de Formula 1! 🏎️💨**
