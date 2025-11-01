# 🏎️ GUÍA RÁPIDA - Video F1 para Reels

## ✅ ¡Tu video ya está listo!

**Ubicación:** `output/f1_racing_video.mp4` (2.3 MB)

## 🎯 Características

- ✅ Formato vertical 1080x1920 (perfecto para reels)
- ✅ 60 FPS (ultra fluido)
- ✅ 15 segundos de duración
- ✅ Calidad máxima (CRF 18)
- ✅ 6 autos F1 animados con colores reales
- ✅ Efectos de velocidad y motion blur
- ✅ Texto dinámico y profesional

## 🚀 Comandos Rápidos

```bash
# Generar nuevo video
npm run generate-video

# Ver opciones de variaciones
npm run variations

# Agregar música (opcional)
npm run add-music /ruta/a/musica.mp3
```

## 📱 Subir a Redes Sociales

### Instagram Reels
1. Abre Instagram → "+" → "Reel"
2. Sube `output/f1_racing_video.mp4`
3. Agrega música trending
4. Hashtags: #F1 #Formula1 #Racing #Speed

### TikTok
1. Abre TikTok → "+" → "Subir"
2. Selecciona el video
3. Usa sonido trending
4. Publica entre 6-9 PM

### YouTube Shorts
1. YouTube Studio → Subir
2. Selecciona el video
3. Título: "F1 Racing - Velocidad Pura 🏎️💨"

## 🎨 Personalizar

Edita `generate-f1-video.js`:

```javascript
// Cambiar duración
duration: 20,  // 20 segundos

// Cambiar FPS
fps: 30,  // 30 FPS (más rápido de generar)

// Cambiar textos
drawText(ctx, 'TU TEXTO', x, y, size, color);

// Agregar más autos
cars.push(new F1Car(x, y, speed, '#color', 'Nombre'));
```

## 💡 Tips para Viralizar

1. **Música:** Usa trending sounds de la plataforma
2. **Hora:** Publica 6-9 PM o 12-2 PM
3. **Hashtags:** Mezcla populares (#F1) con específicos (#MonacoGP)
4. **Descripción:** Corta y con emojis 🏎️💨🔥
5. **Engagement:** Responde comentarios en la primera hora

## 🎵 Agregar Música

```bash
# Descargar música sin copyright de:
# - YouTube Audio Library
# - Epidemic Sound
# - Artlist

# Luego:
node add-music.js /ruta/a/tu/musica.mp3
```

## 📊 Métricas Esperadas

Con buen contenido y timing:
- **Views:** 10K-100K en primeras 24h
- **Engagement:** 5-10% (likes + comentarios)
- **Shares:** 2-5% de los views

## 🔧 Solución Rápida de Problemas

**Video no se genera:**
```bash
npm install
node generate-f1-video.js
```

**Quiero mejor calidad:**
Edita `generate-f1-video.js` → cambia `crf: 15` (más bajo = mejor)

**Quiero archivo más pequeño:**
Edita `generate-f1-video.js` → cambia `crf: 23` (más alto = menor tamaño)

## 📁 Archivos Importantes

- `generate-f1-video.js` - Script principal
- `add-music.js` - Agregar música
- `output/f1_racing_video.mp4` - Tu video final
- `VIDEO_README.md` - Documentación completa

## 🎉 ¡Listo!

Tu video está optimizado y listo para subir. 
¡Que se vuelva viral! 🚀

---

**¿Preguntas?** Lee `VIDEO_README.md` para más detalles.
