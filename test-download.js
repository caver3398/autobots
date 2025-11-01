const fs = require('fs');
const path = require('path');

console.log('🧪 PRUEBA DE RUTAS DE DESCARGA');
console.log('='.repeat(50));
console.log('');

// Verificar archivos
const OUTPUT_DIR = path.join(__dirname, 'output');
const videoPath = path.join(OUTPUT_DIR, 'f1_racing_video.mp4');
const videoWithMusicPath = path.join(OUTPUT_DIR, 'f1_racing_video_with_music.mp4');

console.log('📁 Verificando archivos...');
console.log('');

// Video sin música
if (fs.existsSync(videoPath)) {
  const stats = fs.statSync(videoPath);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  console.log('✅ Video sin música: DISPONIBLE');
  console.log(`   Ruta: ${videoPath}`);
  console.log(`   Tamaño: ${sizeMB} MB`);
  console.log(`   URL descarga: http://localhost:3000/download/video`);
  console.log(`   URL streaming: http://localhost:3000/download/stream/video`);
} else {
  console.log('❌ Video sin música: NO DISPONIBLE');
  console.log('   Genera el video con: npm run generate-video');
}

console.log('');

// Video con música
if (fs.existsSync(videoWithMusicPath)) {
  const stats = fs.statSync(videoWithMusicPath);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  console.log('✅ Video con música: DISPONIBLE');
  console.log(`   Ruta: ${videoWithMusicPath}`);
  console.log(`   Tamaño: ${sizeMB} MB`);
  console.log(`   URL descarga: http://localhost:3000/download/video-with-music`);
  console.log(`   URL streaming: http://localhost:3000/download/stream/video-with-music`);
} else {
  console.log('⚠️  Video con música: NO DISPONIBLE');
  console.log('   Agrega música con: npm run add-music /ruta/a/musica.mp3');
}

console.log('');
console.log('='.repeat(50));
console.log('');
console.log('📋 RUTAS DISPONIBLES:');
console.log('');
console.log('  🌐 Página de descarga:');
console.log('     http://localhost:3000/download');
console.log('');
console.log('  ⬇️  Descarga directa (video sin música):');
console.log('     http://localhost:3000/download/video');
console.log('');
console.log('  ⬇️  Descarga directa (video con música):');
console.log('     http://localhost:3000/download/video-with-music');
console.log('');
console.log('  ▶️  Streaming (video sin música):');
console.log('     http://localhost:3000/download/stream/video');
console.log('');
console.log('  ▶️  Streaming (video con música):');
console.log('     http://localhost:3000/download/stream/video-with-music');
console.log('');
console.log('='.repeat(50));
console.log('');
console.log('🚀 Para iniciar el servidor:');
console.log('   npm start');
console.log('');
console.log('💡 Luego visita: http://localhost:3000/download');
console.log('');
