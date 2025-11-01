const ffmpeg = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const path = require('path');
const fs = require('fs');

ffmpeg.setFfmpegPath(ffmpegPath);

console.log('🎵 AGREGAR MÚSICA AL VIDEO F1');
console.log('='.repeat(50));
console.log('');

const videoPath = path.join(__dirname, 'output', 'f1_racing_video.mp4');
const musicPath = process.argv[2]; // Ruta del archivo de música
const outputPath = path.join(__dirname, 'output', 'f1_racing_video_with_music.mp4');

if (!musicPath) {
  console.log('❌ Error: Debes proporcionar la ruta del archivo de música');
  console.log('');
  console.log('Uso:');
  console.log('  node add-music.js /ruta/a/tu/musica.mp3');
  console.log('');
  console.log('Formatos soportados: MP3, WAV, AAC, M4A, OGG');
  console.log('');
  console.log('Consejos:');
  console.log('  - Usa música sin copyright para evitar problemas');
  console.log('  - Sitios recomendados: YouTube Audio Library, Epidemic Sound');
  console.log('  - La música se ajustará automáticamente a la duración del video');
  console.log('');
  process.exit(1);
}

if (!fs.existsSync(musicPath)) {
  console.log(`❌ Error: No se encuentra el archivo de música: ${musicPath}`);
  process.exit(1);
}

if (!fs.existsSync(videoPath)) {
  console.log(`❌ Error: No se encuentra el video: ${videoPath}`);
  console.log('   Primero genera el video con: node generate-f1-video.js');
  process.exit(1);
}

console.log('📹 Video:', videoPath);
console.log('🎵 Música:', musicPath);
console.log('💾 Salida:', outputPath);
console.log('');
console.log('⏳ Procesando...');
console.log('');

ffmpeg()
  .input(videoPath)
  .input(musicPath)
  .outputOptions([
    '-c:v copy', // Copiar video sin re-encodear (más rápido)
    '-c:a aac', // Codec de audio
    '-b:a 192k', // Bitrate de audio
    '-shortest', // Cortar al más corto (video o música)
    '-map 0:v:0', // Mapear video del primer input
    '-map 1:a:0' // Mapear audio del segundo input
  ])
  .output(outputPath)
  .on('start', (commandLine) => {
    console.log('Comando FFmpeg:', commandLine);
    console.log('');
  })
  .on('progress', (progress) => {
    if (progress.percent) {
      console.log(`Progreso: ${Math.round(progress.percent)}%`);
    }
  })
  .on('end', () => {
    console.log('');
    console.log('✅ ¡Video con música creado exitosamente!');
    console.log('');
    console.log(`📁 Ubicación: ${outputPath}`);
    console.log('');
    console.log('🎉 ¡Listo para subir a redes sociales!');
  })
  .on('error', (err) => {
    console.error('');
    console.error('❌ Error al agregar música:', err.message);
    console.error('');
    console.error('Posibles soluciones:');
    console.error('  - Verifica que el archivo de música sea válido');
    console.error('  - Intenta con otro formato de audio (MP3, WAV)');
    console.error('  - Asegúrate de tener espacio en disco');
  })
  .run();
