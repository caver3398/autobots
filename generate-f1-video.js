const { createCanvas, registerFont } = require('canvas');
const fs = require('fs');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');

ffmpeg.setFfmpegPath(ffmpegPath);

// Configuración del video
const CONFIG = {
  width: 1080,
  height: 1920,
  fps: 60,
  duration: 15, // segundos
  outputDir: path.join(__dirname, 'output'),
  framesDir: path.join(__dirname, 'output', 'frames')
};

// Crear directorios si no existen
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}
if (!fs.existsSync(CONFIG.framesDir)) {
  fs.mkdirSync(CONFIG.framesDir, { recursive: true });
}

// Clase para representar un auto de F1
class F1Car {
  constructor(x, y, speed, color, teamName) {
    this.x = x;
    this.y = y;
    this.speed = speed;
    this.color = color;
    this.teamName = teamName;
    this.width = 180;
    this.height = 80;
  }

  update() {
    this.x += this.speed;
    if (this.x > CONFIG.width + 200) {
      this.x = -200;
    }
  }

  draw(ctx) {
    ctx.save();
    
    // Sombra del auto
    ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
    ctx.shadowBlur = 20;
    ctx.shadowOffsetX = 5;
    ctx.shadowOffsetY = 5;

    // Cuerpo principal del auto
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(this.x, this.y);
    ctx.lineTo(this.x + this.width * 0.8, this.y);
    ctx.lineTo(this.x + this.width, this.y + this.height * 0.5);
    ctx.lineTo(this.x + this.width * 0.8, this.y + this.height);
    ctx.lineTo(this.x, this.y + this.height);
    ctx.lineTo(this.x + this.width * 0.2, this.y + this.height * 0.5);
    ctx.closePath();
    ctx.fill();

    // Detalles del auto
    ctx.shadowBlur = 0;
    
    // Cabina
    ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
    ctx.fillRect(this.x + this.width * 0.3, this.y + this.height * 0.2, this.width * 0.3, this.height * 0.6);

    // Alerón trasero
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x - 20, this.y + this.height * 0.1, 25, this.height * 0.8);

    // Alerón delantero
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x + this.width - 5, this.y + this.height * 0.2, 15, this.height * 0.6);

    // Líneas de velocidad (motion blur)
    ctx.strokeStyle = `${this.color}40`;
    ctx.lineWidth = 3;
    for (let i = 0; i < 5; i++) {
      ctx.beginPath();
      ctx.moveTo(this.x - 50 - i * 20, this.y + this.height * 0.3 + i * 10);
      ctx.lineTo(this.x - 100 - i * 20, this.y + this.height * 0.3 + i * 10);
      ctx.stroke();
    }

    ctx.restore();
  }
}

// Función para dibujar el fondo de pista
function drawTrack(ctx, frame) {
  // Gradiente de fondo
  const gradient = ctx.createLinearGradient(0, 0, 0, CONFIG.height);
  gradient.addColorStop(0, '#0a0a0a');
  gradient.addColorStop(0.5, '#1a1a1a');
  gradient.addColorStop(1, '#0a0a0a');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, CONFIG.width, CONFIG.height);

  // Líneas de la pista (animadas)
  const lineOffset = (frame * 15) % 100;
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 8;
  ctx.setLineDash([50, 50]);
  ctx.lineDashOffset = -lineOffset;
  
  // Línea central
  ctx.beginPath();
  ctx.moveTo(CONFIG.width / 2, 0);
  ctx.lineTo(CONFIG.width / 2, CONFIG.height);
  ctx.stroke();

  // Bordes de la pista
  ctx.strokeStyle = '#ff0000';
  ctx.lineWidth = 12;
  ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(100, 0);
  ctx.lineTo(100, CONFIG.height);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(CONFIG.width - 100, 0);
  ctx.lineTo(CONFIG.width - 100, CONFIG.height);
  ctx.stroke();

  // Líneas de borde blancas
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(110, 0);
  ctx.lineTo(110, CONFIG.height);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(CONFIG.width - 110, 0);
  ctx.lineTo(CONFIG.width - 110, CONFIG.height);
  ctx.stroke();
}

// Función para dibujar texto con efectos
function drawText(ctx, text, x, y, size, color, shadow = true) {
  ctx.save();
  
  if (shadow) {
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 15;
    ctx.shadowOffsetX = 3;
    ctx.shadowOffsetY = 3;
  }

  ctx.font = `bold ${size}px Arial, sans-serif`;
  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.fillText(text, x, y);

  // Borde del texto
  ctx.strokeStyle = '#000000';
  ctx.lineWidth = 3;
  ctx.strokeText(text, x, y);

  ctx.restore();
}

// Función para dibujar efectos de partículas
function drawParticles(ctx, frame) {
  const particleCount = 50;
  for (let i = 0; i < particleCount; i++) {
    const x = (frame * 5 + i * 50) % CONFIG.width;
    const y = Math.random() * CONFIG.height;
    const size = Math.random() * 3 + 1;
    const opacity = Math.random() * 0.5;

    ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fill();
  }
}

// Generar frames
async function generateFrames() {
  console.log('🎬 Generando frames del video de F1...');
  
  const canvas = createCanvas(CONFIG.width, CONFIG.height);
  const ctx = canvas.getContext('2d');
  
  const totalFrames = CONFIG.fps * CONFIG.duration;

  // Crear autos de F1 con colores de equipos reales
  const cars = [
    new F1Car(200, 400, 12, '#e10600', 'Ferrari'),
    new F1Car(-100, 600, 15, '#0090ff', 'Alpine'),
    new F1Car(400, 800, 10, '#00d2be', 'Mercedes'),
    new F1Car(-300, 1000, 13, '#0600ef', 'Red Bull'),
    new F1Car(100, 1200, 11, '#ff8700', 'McLaren'),
    new F1Car(-200, 1400, 14, '#006f62', 'Aston Martin')
  ];

  for (let frame = 0; frame < totalFrames; frame++) {
    // Limpiar canvas
    ctx.clearRect(0, 0, CONFIG.width, CONFIG.height);

    // Dibujar fondo de pista
    drawTrack(ctx, frame);

    // Dibujar partículas de velocidad
    drawParticles(ctx, frame);

    // Actualizar y dibujar autos
    cars.forEach(car => {
      car.update();
      car.draw(ctx);
    });

    // Título principal (aparece gradualmente)
    const titleOpacity = Math.min(frame / 60, 1);
    if (frame < 180) {
      ctx.globalAlpha = titleOpacity;
      drawText(ctx, 'FORMULA 1', CONFIG.width / 2, 200, 80, '#ffffff');
      drawText(ctx, 'RACING', CONFIG.width / 2, 300, 60, '#e10600');
      ctx.globalAlpha = 1;
    }

    // Información de carrera (segunda mitad del video)
    if (frame > 180) {
      const infoOpacity = Math.min((frame - 180) / 60, 1);
      ctx.globalAlpha = infoOpacity;
      
      // Fondo semi-transparente para el texto
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      ctx.fillRect(0, 100, CONFIG.width, 400);
      
      drawText(ctx, 'VELOCIDAD MÁXIMA', CONFIG.width / 2, 200, 50, '#ffffff');
      drawText(ctx, '372 KM/H', CONFIG.width / 2, 280, 70, '#e10600');
      drawText(ctx, 'ADRENALINA PURA', CONFIG.width / 2, 380, 45, '#ffffff');
      
      ctx.globalAlpha = 1;
    }

    // Contador de velocidad
    const speed = 200 + Math.sin(frame / 30) * 50;
    drawText(ctx, `${Math.round(speed)} KM/H`, CONFIG.width / 2, CONFIG.height - 150, 50, '#00ff00', false);

    // Barra de progreso
    const progress = frame / totalFrames;
    ctx.fillStyle = '#e10600';
    ctx.fillRect(50, CONFIG.height - 80, (CONFIG.width - 100) * progress, 10);
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.strokeRect(50, CONFIG.height - 80, CONFIG.width - 100, 10);

    // Guardar frame
    const buffer = canvas.toBuffer('image/png');
    const framePath = path.join(CONFIG.framesDir, `frame_${String(frame).padStart(5, '0')}.png`);
    fs.writeFileSync(framePath, buffer);

    // Mostrar progreso
    if (frame % 60 === 0) {
      console.log(`   Progreso: ${Math.round((frame / totalFrames) * 100)}%`);
    }
  }

  console.log('✅ Frames generados exitosamente!');
}

// Compilar frames en video
async function compileVideo() {
  console.log('🎥 Compilando video...');

  const outputPath = path.join(CONFIG.outputDir, 'f1_racing_video.mp4');

  return new Promise((resolve, reject) => {
    ffmpeg()
      .input(path.join(CONFIG.framesDir, 'frame_%05d.png'))
      .inputFPS(CONFIG.fps)
      .videoCodec('libx264')
      .outputOptions([
        '-pix_fmt yuv420p',
        '-crf 18', // Calidad alta (0-51, menor = mejor calidad)
        '-preset slow', // Mejor compresión
        '-movflags +faststart' // Optimización para streaming
      ])
      .output(outputPath)
      .on('start', (commandLine) => {
        console.log('   Comando FFmpeg:', commandLine);
      })
      .on('progress', (progress) => {
        if (progress.percent) {
          console.log(`   Progreso: ${Math.round(progress.percent)}%`);
        }
      })
      .on('end', () => {
        console.log('✅ Video compilado exitosamente!');
        console.log(`📁 Ubicación: ${outputPath}`);
        resolve(outputPath);
      })
      .on('error', (err) => {
        console.error('❌ Error al compilar video:', err);
        reject(err);
      })
      .run();
  });
}

// Limpiar frames temporales
function cleanupFrames() {
  console.log('🧹 Limpiando frames temporales...');
  const files = fs.readdirSync(CONFIG.framesDir);
  files.forEach(file => {
    fs.unlinkSync(path.join(CONFIG.framesDir, file));
  });
  fs.rmdirSync(CONFIG.framesDir);
  console.log('✅ Limpieza completada!');
}

// Función principal
async function main() {
  console.log('🏎️  GENERADOR DE VIDEO F1 - ALTA CALIDAD 🏎️');
  console.log('='.repeat(50));
  console.log(`Resolución: ${CONFIG.width}x${CONFIG.height}`);
  console.log(`FPS: ${CONFIG.fps}`);
  console.log(`Duración: ${CONFIG.duration} segundos`);
  console.log('='.repeat(50));
  console.log('');

  try {
    await generateFrames();
    await compileVideo();
    cleanupFrames();
    
    console.log('');
    console.log('🎉 ¡VIDEO GENERADO EXITOSAMENTE! 🎉');
    console.log('');
    console.log('El video está listo para subir como reel.');
    console.log('Características:');
    console.log('  ✓ Formato vertical (1080x1920)');
    console.log('  ✓ 60 FPS para fluidez máxima');
    console.log('  ✓ Calidad alta (CRF 18)');
    console.log('  ✓ Animaciones de autos F1');
    console.log('  ✓ Efectos visuales dinámicos');
    console.log('');
  } catch (error) {
    console.error('❌ Error durante la generación:', error);
    process.exit(1);
  }
}

// Ejecutar
main();
