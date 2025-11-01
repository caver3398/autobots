const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🎬 GENERADOR DE VARIACIONES DE VIDEO F1');
console.log('='.repeat(50));
console.log('');
console.log('Este script te permite generar diferentes versiones del video.');
console.log('');

const variations = [
  {
    name: 'Versión Corta (10 segundos)',
    duration: 10,
    fps: 60,
    description: 'Perfecta para TikTok y Reels rápidos'
  },
  {
    name: 'Versión Larga (30 segundos)',
    duration: 30,
    fps: 60,
    description: 'Más contenido y animaciones'
  },
  {
    name: 'Versión Ultra Suave (120 FPS)',
    duration: 15,
    fps: 120,
    description: 'Máxima fluidez (requiere más tiempo)'
  },
  {
    name: 'Versión Estándar (30 FPS)',
    duration: 15,
    fps: 30,
    description: 'Generación más rápida, menor tamaño'
  }
];

console.log('Variaciones disponibles:');
console.log('');
variations.forEach((v, i) => {
  console.log(`${i + 1}. ${v.name}`);
  console.log(`   - Duración: ${v.duration}s`);
  console.log(`   - FPS: ${v.fps}`);
  console.log(`   - ${v.description}`);
  console.log('');
});

console.log('Para generar una variación, edita generate-f1-video.js');
console.log('y modifica los valores en CONFIG:');
console.log('');
console.log('const CONFIG = {');
console.log('  duration: 10,  // Cambia la duración');
console.log('  fps: 60,       // Cambia los FPS');
console.log('  // ...');
console.log('};');
console.log('');
console.log('Luego ejecuta: node generate-f1-video.js');
