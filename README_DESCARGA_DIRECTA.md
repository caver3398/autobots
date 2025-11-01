# 🎬 Sistema de Descarga Directa de Videos F1

## ✨ ¿Qué es esto?

Sistema completo para **descargar videos de Formula 1 con audio** directamente desde tu navegador o línea de comandos.

---

## 🚀 Inicio Rápido (3 pasos)

### 1. Inicia el servidor
```bash
npm start
```

### 2. Abre tu navegador
```
http://localhost:3000/download
```

### 3. Haz clic en "Descargar Video"
¡Listo! El video se descargará automáticamente a tu computadora.

---

## 📥 Métodos de Descarga

### 🌐 Método 1: Interfaz Web (Recomendado)

La forma más fácil:

1. Abre: `http://localhost:3000/download`
2. Verás una página con botones de descarga
3. Haz clic en el botón del video que quieras
4. El video se descargará automáticamente

**Características:**
- ✅ Interfaz visual amigable
- ✅ Muestra información del video (tamaño, duración, etc.)
- ✅ Botones para descargar o ver online
- ✅ Instrucciones integradas

### 🔗 Método 2: Enlaces Directos

Copia y pega estos enlaces en tu navegador:

**Video sin música:**
```
http://localhost:3000/download/video
```

**Video con música:**
```
http://localhost:3000/download/video-with-music
```

### 💻 Método 3: Línea de Comandos

**Con curl:**
```bash
curl -o f1_video.mp4 http://localhost:3000/download/video
```

**Con wget:**
```bash
wget http://localhost:3000/download/video
```

### ▶️ Método 4: Ver Online (Streaming)

Para ver el video en tu navegador sin descargar:

```
http://localhost:3000/download/stream/video
```

---

## 🎵 Agregar Música al Video

Si quieres descargar el video **con música**:

```bash
npm run add-music /ruta/a/tu/musica.mp3
```

Luego podrás descargarlo desde:
```
http://localhost:3000/download/video-with-music
```

### Fuentes de Música Sin Copyright:
- [YouTube Audio Library](https://studio.youtube.com/)
- [Epidemic Sound](https://www.epidemicsound.com/)
- [Free Music Archive](https://freemusicarchive.org/)

---

## 📊 Verificar Videos Disponibles

Para ver qué videos están listos para descargar:

```bash
npm run check-downloads
```

Esto mostrará:
- ✅ Qué videos están disponibles
- 📊 Tamaño de cada video
- 🔗 URLs de descarga directa

---

## 📱 Compartir en Redes Sociales

Una vez descargado el video:

### Instagram Reels
1. Abre Instagram → "+" → Reel
2. Sube el video descargado
3. Agrega hashtags: `#F1 #Formula1 #Racing`
4. ¡Publica!

### TikTok
1. Abre TikTok → "+" → Subir
2. Selecciona el video
3. ¡Publica!

### YouTube Shorts
1. YouTube Studio → Subir
2. Selecciona el video
3. Marca como "Short"
4. ¡Publica!

---

## 🎯 Características del Video

### Video Sin Música
- **Formato:** MP4 (H.264)
- **Resolución:** 1080x1920 (vertical)
- **FPS:** 60
- **Duración:** 15 segundos
- **Tamaño:** ~2.3 MB
- **Calidad:** Alta (CRF 18)

### Contenido:
- ✅ 6 autos F1 animados (Ferrari, Alpine, Mercedes, Red Bull, McLaren, Aston Martin)
- ✅ Efectos de velocidad y motion blur
- ✅ Texto dinámico con información
- ✅ Pista de carreras animada
- ✅ Optimizado para redes sociales

---

## 🛠️ Comandos Útiles

```bash
# Generar video F1
npm run generate-video

# Agregar música
npm run add-music /ruta/a/musica.mp3

# Ver videos disponibles
npm run check-downloads

# Iniciar servidor
npm start

# Ver ejemplos de descarga
./EJEMPLOS_DESCARGA.sh
```

---

## 🔧 Rutas de la API

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/download` | GET | Página web con interfaz de descarga |
| `/download/video` | GET | Descarga directa del video sin música |
| `/download/video-with-music` | GET | Descarga directa del video con música |
| `/download/stream/video` | GET | Streaming del video sin música |
| `/download/stream/video-with-music` | GET | Streaming del video con música |

---

## 📚 Documentación Adicional

- **[INSTRUCCIONES_DESCARGA.md](INSTRUCCIONES_DESCARGA.md)** - Guía rápida de 3 pasos
- **[DESCARGA_README.md](DESCARGA_README.md)** - Documentación técnica completa
- **[EJEMPLOS_DESCARGA.sh](EJEMPLOS_DESCARGA.sh)** - Ejemplos de uso con curl/wget
- **[VIDEO_README.md](VIDEO_README.md)** - Información sobre generación de videos

---

## 🆘 Solución de Problemas

### ❌ "Video no encontrado"

**Problema:** El video no ha sido generado.

**Solución:**
```bash
npm run generate-video
```

### ❌ "Video con música no encontrado"

**Problema:** No se ha agregado música al video.

**Solución:**
```bash
npm run add-music /ruta/a/musica.mp3
```

### ❌ "Cannot GET /download"

**Problema:** El servidor no está corriendo.

**Solución:**
```bash
npm start
```

### ❌ El video se reproduce en lugar de descargarse

**Problema:** El navegador está configurado para reproducir MP4.

**Solución:** 
- Usa las rutas de descarga directa
- O haz clic derecho → "Guardar como"

---

## 💡 Consejos Pro

1. **Calidad:** Los videos están optimizados para redes sociales (alta calidad, tamaño pequeño)

2. **Música:** Usa música sin copyright para evitar problemas de derechos de autor

3. **Hashtags:** Usa hashtags relevantes: `#F1 #Formula1 #Racing #Speed #Motorsport`

4. **Horario:** Publica entre 6-9 PM para máximo alcance

5. **Tendencias:** Usa sonidos trending de tu plataforma

---

## 🎉 ¡Listo!

Ahora puedes:
- ✅ Descargar videos de F1 de alta calidad
- ✅ Agregar música personalizada
- ✅ Ver videos en streaming
- ✅ Compartir en redes sociales
- ✅ Usar desde navegador o línea de comandos

---

## 📞 Soporte

Si tienes problemas:

1. Ejecuta: `npm run check-downloads`
2. Verifica que el servidor esté corriendo: `npm start`
3. Lee la documentación completa: `DESCARGA_README.md`

---

**¡Disfruta creando contenido viral de Formula 1! 🏎️💨**

---

## 📦 Archivos del Sistema

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
├── test-download.js                      # Script de verificación
├── INSTRUCCIONES_DESCARGA.md             # Guía rápida
├── DESCARGA_README.md                    # Documentación completa
└── EJEMPLOS_DESCARGA.sh                  # Ejemplos de uso
```

---

**Creado con ❤️ para amantes de la velocidad y Formula 1**
