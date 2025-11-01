# 🏎️ Generador de Video F1 - Alta Calidad

## 📹 Video Generado

Tu video de Formula 1 ha sido creado exitosamente y está listo para subir como reel!

**Ubicación:** `output/f1_racing_video.mp4`

## ✨ Características del Video

- **Formato:** Vertical (1080x1920) - Perfecto para Instagram Reels, TikTok, YouTube Shorts
- **Calidad:** Alta (CRF 18) - Máxima calidad visual
- **FPS:** 60 frames por segundo - Fluidez ultra suave
- **Duración:** 15 segundos
- **Tamaño:** ~2.3 MB - Optimizado para redes sociales
- **Codec:** H.264 (compatible con todas las plataformas)

## 🎨 Contenido del Video

El video incluye:

1. **Animaciones de Autos F1:**
   - 6 autos de equipos reales (Ferrari, Alpine, Mercedes, Red Bull, McLaren, Aston Martin)
   - Colores oficiales de los equipos
   - Movimiento fluido y realista

2. **Efectos Visuales:**
   - Pista de carreras animada con líneas en movimiento
   - Efectos de velocidad (motion blur)
   - Partículas de velocidad
   - Sombras y profundidad

3. **Texto Dinámico:**
   - Título "FORMULA 1 RACING"
   - Información de velocidad máxima (372 KM/H)
   - Contador de velocidad en tiempo real
   - Barra de progreso

4. **Diseño Profesional:**
   - Gradientes de color
   - Transiciones suaves
   - Tipografía bold con sombras
   - Composición vertical optimizada

## 🚀 Cómo Usar

### Generar un Nuevo Video

```bash
node generate-f1-video.js
```

El script:
1. Genera 900 frames (15 segundos × 60 FPS)
2. Compila los frames en video MP4
3. Limpia archivos temporales automáticamente

### Personalizar el Video

Puedes editar `generate-f1-video.js` para personalizar:

```javascript
const CONFIG = {
  width: 1080,        // Ancho del video
  height: 1920,       // Alto del video
  fps: 60,            // Frames por segundo
  duration: 15,       // Duración en segundos
  // ...
};
```

#### Cambiar Colores de Autos:

```javascript
const cars = [
  new F1Car(200, 400, 12, '#e10600', 'Ferrari'),  // Rojo Ferrari
  new F1Car(-100, 600, 15, '#0090ff', 'Alpine'),  // Azul Alpine
  // Agrega más o modifica los existentes
];
```

#### Modificar Textos:

Busca las funciones `drawText()` en el código y cambia los textos:

```javascript
drawText(ctx, 'TU TEXTO AQUÍ', CONFIG.width / 2, 200, 80, '#ffffff');
```

## 📱 Subir a Redes Sociales

### Instagram Reels
1. Abre Instagram
2. Toca el botón "+"
3. Selecciona "Reel"
4. Sube `f1_racing_video.mp4`
5. Agrega música si deseas
6. ¡Publica!

### TikTok
1. Abre TikTok
2. Toca el botón "+"
3. Selecciona "Subir"
4. Elige `f1_racing_video.mp4`
5. Edita y publica

### YouTube Shorts
1. Abre YouTube Studio
2. Crea → Subir videos
3. Selecciona `f1_racing_video.mp4`
4. Agrega título y descripción
5. Publica como Short

## 🎯 Consejos para Máximo Engagement

1. **Música:** Agrega música de alta energía (trap, EDM, rock)
2. **Hashtags:** #F1 #Formula1 #Racing #Speed #Motorsport
3. **Descripción:** "Velocidad pura 🏎️💨 372 KM/H de adrenalina"
4. **Mejor Hora:** Publica entre 6-9 PM para máximo alcance
5. **Tendencias:** Usa sonidos trending de tu plataforma

## 🔧 Requisitos Técnicos

- Node.js (v12 o superior)
- Dependencias instaladas:
  - `canvas` - Renderizado de gráficos
  - `fluent-ffmpeg` - Procesamiento de video
  - `ffmpeg-static` - Binario de FFmpeg

## 📊 Especificaciones Técnicas

- **Codec de Video:** H.264 (libx264)
- **Formato de Píxeles:** YUV420P
- **CRF:** 18 (calidad muy alta)
- **Preset:** Slow (mejor compresión)
- **Optimización:** Fast start habilitado (streaming)

## 🎨 Personalización Avanzada

### Agregar Más Autos

```javascript
cars.push(new F1Car(x, y, velocidad, '#color', 'Nombre'));
```

### Cambiar Velocidad de Animación

Modifica el parámetro `speed` en cada auto:
- Valores más altos = más rápido
- Valores recomendados: 10-15

### Ajustar Efectos Visuales

- **Partículas:** Modifica `particleCount` en `drawParticles()`
- **Motion Blur:** Ajusta el loop en el método `draw()` de F1Car
- **Sombras:** Cambia `shadowBlur` y `shadowColor`

## 🐛 Solución de Problemas

### El video no se genera
- Verifica que las dependencias estén instaladas: `npm install`
- Asegúrate de tener espacio en disco suficiente

### Calidad baja
- Reduce el valor de CRF (mínimo 0, máximo 51)
- Aumenta el FPS (30, 60, 120)

### Video muy pesado
- Aumenta el valor de CRF (18-23 recomendado)
- Cambia preset a 'medium' o 'fast'

## 📝 Notas

- La generación toma aproximadamente 1-2 minutos
- Se crean frames temporales que se eliminan automáticamente
- El video final está optimizado para redes sociales

## 🎉 ¡Listo para Viralizar!

Tu video de F1 está optimizado para máximo impacto en redes sociales. 
¡Súbelo y disfruta del engagement! 🚀

---

**Creado con ❤️ para amantes de la velocidad y Formula 1**
