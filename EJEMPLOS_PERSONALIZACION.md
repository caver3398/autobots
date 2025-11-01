# 🎨 Ejemplos de Personalización

## 1. Cambiar Colores de Autos

```javascript
// En generate-f1-video.js, busca la sección de autos y modifica:

const cars = [
  // Colores personalizados
  new F1Car(200, 400, 12, '#ff0000', 'Rojo Fuego'),
  new F1Car(-100, 600, 15, '#00ff00', 'Verde Neón'),
  new F1Car(400, 800, 10, '#ffff00', 'Amarillo Eléctrico'),
  new F1Car(-300, 1000, 13, '#ff00ff', 'Magenta'),
  new F1Car(100, 1200, 11, '#00ffff', 'Cyan'),
  new F1Car(-200, 1400, 14, '#ffffff', 'Blanco Puro')
];
```

## 2. Cambiar Textos

```javascript
// Título principal (línea ~180)
drawText(ctx, 'SUPER CARRERAS', CONFIG.width / 2, 200, 80, '#ffffff');
drawText(ctx, 'VELOCIDAD EXTREMA', CONFIG.width / 2, 300, 60, '#e10600');

// Información de velocidad (línea ~200)
drawText(ctx, 'VELOCIDAD RÉCORD', CONFIG.width / 2, 200, 50, '#ffffff');
drawText(ctx, '400 KM/H', CONFIG.width / 2, 280, 70, '#e10600');
drawText(ctx, '¡PURA ADRENALINA!', CONFIG.width / 2, 380, 45, '#ffffff');
```

## 3. Ajustar Duración y FPS

```javascript
// Para video más corto (10 segundos)
const CONFIG = {
  width: 1080,
  height: 1920,
  fps: 60,
  duration: 10,  // ← Cambia aquí
  // ...
};

// Para video más fluido (120 FPS)
const CONFIG = {
  width: 1080,
  height: 1920,
  fps: 120,  // ← Cambia aquí
  duration: 15,
  // ...
};

// Para generación más rápida (30 FPS)
const CONFIG = {
  width: 1080,
  height: 1920,
  fps: 30,  // ← Cambia aquí
  duration: 15,
  // ...
};
```

## 4. Cambiar Velocidad de Autos

```javascript
// Autos más rápidos
const cars = [
  new F1Car(200, 400, 20, '#e10600', 'Ferrari'),  // speed: 20 (muy rápido)
  new F1Car(-100, 600, 25, '#0090ff', 'Alpine'),  // speed: 25 (ultra rápido)
  // ...
];

// Autos más lentos (más control visual)
const cars = [
  new F1Car(200, 400, 5, '#e10600', 'Ferrari'),   // speed: 5 (lento)
  new F1Car(-100, 600, 7, '#0090ff', 'Alpine'),   // speed: 7 (moderado)
  // ...
];
```

## 5. Cambiar Calidad del Video

```javascript
// En la función compileVideo(), busca outputOptions:

// MÁXIMA CALIDAD (archivo más grande)
.outputOptions([
  '-pix_fmt yuv420p',
  '-crf 15',        // ← Cambia de 18 a 15
  '-preset slower', // ← Cambia de slow a slower
  '-movflags +faststart'
])

// CALIDAD MEDIA (archivo más pequeño)
.outputOptions([
  '-pix_fmt yuv420p',
  '-crf 23',        // ← Cambia de 18 a 23
  '-preset medium', // ← Cambia de slow a medium
  '-movflags +faststart'
])

// CALIDAD BAJA (archivo muy pequeño, generación rápida)
.outputOptions([
  '-pix_fmt yuv420p',
  '-crf 28',        // ← Cambia de 18 a 28
  '-preset fast',   // ← Cambia de slow a fast
  '-movflags +faststart'
])
```

## 6. Agregar Más Autos

```javascript
const cars = [
  // Autos existentes...
  new F1Car(200, 400, 12, '#e10600', 'Ferrari'),
  new F1Car(-100, 600, 15, '#0090ff', 'Alpine'),
  
  // Agregar nuevos autos
  new F1Car(300, 1600, 16, '#purple', 'Equipo Morado'),
  new F1Car(-150, 1750, 14, '#gold', 'Equipo Dorado'),
  new F1Car(50, 1900, 13, '#silver', 'Equipo Plateado'),
];
```

## 7. Cambiar Fondo de Pista

```javascript
// En la función drawTrack(), modifica los colores:

// Fondo oscuro (actual)
const gradient = ctx.createLinearGradient(0, 0, 0, CONFIG.height);
gradient.addColorStop(0, '#0a0a0a');
gradient.addColorStop(0.5, '#1a1a1a');
gradient.addColorStop(1, '#0a0a0a');

// Fondo azul nocturno
const gradient = ctx.createLinearGradient(0, 0, 0, CONFIG.height);
gradient.addColorStop(0, '#001a33');
gradient.addColorStop(0.5, '#003366');
gradient.addColorStop(1, '#001a33');

// Fondo rojo intenso
const gradient = ctx.createLinearGradient(0, 0, 0, CONFIG.height);
gradient.addColorStop(0, '#330000');
gradient.addColorStop(0.5, '#660000');
gradient.addColorStop(1, '#330000');
```

## 8. Modificar Efectos de Partículas

```javascript
// En la función drawParticles():

// Más partículas (más efecto)
const particleCount = 100;  // ← Cambia de 50 a 100

// Partículas más grandes
const size = Math.random() * 6 + 2;  // ← Cambia de 3+1 a 6+2

// Partículas más visibles
const opacity = Math.random() * 0.8;  // ← Cambia de 0.5 a 0.8
```

## 9. Cambiar Tamaño de Autos

```javascript
// En la clase F1Car, constructor:

constructor(x, y, speed, color, teamName) {
  this.x = x;
  this.y = y;
  this.speed = speed;
  this.color = color;
  this.teamName = teamName;
  this.width = 250;   // ← Cambia de 180 a 250 (más grande)
  this.height = 110;  // ← Cambia de 80 a 110 (más grande)
}

// O más pequeños:
  this.width = 120;   // ← Más pequeño
  this.height = 50;   // ← Más pequeño
```

## 10. Formato Horizontal (YouTube)

```javascript
// Para video horizontal en lugar de vertical:

const CONFIG = {
  width: 1920,   // ← Cambia de 1080 a 1920
  height: 1080,  // ← Cambia de 1920 a 1080
  fps: 60,
  duration: 15,
  // ...
};
```

## 11. Agregar Logo o Marca de Agua

```javascript
// En la función generateFrames(), después de dibujar los autos:

// Logo de texto
drawText(ctx, '@TuUsuario', CONFIG.width - 150, CONFIG.height - 50, 30, '#ffffff');

// O con fondo
ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
ctx.fillRect(CONFIG.width - 250, CONFIG.height - 80, 230, 60);
drawText(ctx, '@TuUsuario', CONFIG.width - 135, CONFIG.height - 40, 30, '#ffffff');
```

## 12. Cambiar Colores del Texto

```javascript
// Texto con gradiente (requiere más código)
// O simplemente cambiar colores:

drawText(ctx, 'FORMULA 1', CONFIG.width / 2, 200, 80, '#00ff00');  // Verde
drawText(ctx, 'RACING', CONFIG.width / 2, 300, 60, '#ffff00');     // Amarillo
```

## 13. Video Cuadrado (Instagram Post)

```javascript
const CONFIG = {
  width: 1080,   // ← Cuadrado
  height: 1080,  // ← Cuadrado
  fps: 60,
  duration: 15,
  // ...
};
```

## 14. Ajustar Motion Blur

```javascript
// En el método draw() de F1Car, busca el loop de líneas:

// Más motion blur
for (let i = 0; i < 10; i++) {  // ← Cambia de 5 a 10
  ctx.beginPath();
  ctx.moveTo(this.x - 50 - i * 30, this.y + this.height * 0.3 + i * 10);
  ctx.lineTo(this.x - 150 - i * 30, this.y + this.height * 0.3 + i * 10);
  ctx.stroke();
}

// Menos motion blur
for (let i = 0; i < 3; i++) {  // ← Cambia de 5 a 3
  // ...
}
```

## 15. Cambiar Barra de Progreso

```javascript
// Color diferente
ctx.fillStyle = '#00ff00';  // Verde en lugar de rojo

// Posición diferente (arriba)
ctx.fillRect(50, 50, (CONFIG.width - 100) * progress, 10);
ctx.strokeRect(50, 50, CONFIG.width - 100, 10);

// Más gruesa
ctx.fillRect(50, CONFIG.height - 80, (CONFIG.width - 100) * progress, 20);  // 20 en lugar de 10
```

## 🎯 Combinaciones Recomendadas

### Para TikTok (Rápido y Dinámico)
```javascript
duration: 10,
fps: 60,
crf: 20,
// Autos muy rápidos (speed: 20-25)
// Muchas partículas (100+)
```

### Para Instagram Reels (Calidad Premium)
```javascript
duration: 15,
fps: 60,
crf: 15,
// Autos moderados (speed: 12-15)
// Efectos balanceados
```

### Para YouTube Shorts (Largo y Detallado)
```javascript
duration: 30,
fps: 60,
crf: 18,
// Más contenido y transiciones
// Texto más elaborado
```

## 💡 Tips

1. **Prueba cambios pequeños primero** - Genera videos cortos (5s) para probar
2. **Guarda versiones** - Copia el archivo antes de modificar
3. **Experimenta con colores** - Los colores brillantes funcionan mejor
4. **Ajusta según plataforma** - Cada red social tiene preferencias diferentes

## 🚀 Genera y Prueba

Después de cada cambio:
```bash
node generate-f1-video.js
```

¡Experimenta y crea tu video único! 🎨
