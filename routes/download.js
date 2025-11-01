const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');

// Directorio de salida de videos
const OUTPUT_DIR = path.join(__dirname, '..', 'output');

/* GET página de descarga */
router.get('/', function(req, res) {
  // Verificar qué videos están disponibles
  const videoPath = path.join(OUTPUT_DIR, 'f1_racing_video.mp4');
  const videoWithMusicPath = path.join(OUTPUT_DIR, 'f1_racing_video_with_music.mp4');
  
  const videoExists = fs.existsSync(videoPath);
  const videoWithMusicExists = fs.existsSync(videoWithMusicPath);
  
  // Obtener tamaños de archivo si existen
  let videoSize = null;
  let videoWithMusicSize = null;
  
  if (videoExists) {
    const stats = fs.statSync(videoPath);
    videoSize = (stats.size / (1024 * 1024)).toFixed(2); // MB
  }
  
  if (videoWithMusicExists) {
    const stats = fs.statSync(videoWithMusicPath);
    videoWithMusicSize = (stats.size / (1024 * 1024)).toFixed(2); // MB
  }
  
  res.render('download', {
    title: 'Descargar Videos F1',
    videoExists: videoExists,
    videoWithMusicExists: videoWithMusicExists,
    videoSize: videoSize,
    videoWithMusicSize: videoWithMusicSize
  });
});

/* GET descargar video sin música */
router.get('/video', function(req, res) {
  const videoPath = path.join(OUTPUT_DIR, 'f1_racing_video.mp4');
  
  // Verificar si el archivo existe
  if (!fs.existsSync(videoPath)) {
    return res.status(404).send('Video no encontrado. Por favor, genera el video primero usando: node generate-f1-video.js');
  }
  
  // Configurar headers para descarga
  res.setHeader('Content-Type', 'video/mp4');
  res.setHeader('Content-Disposition', 'attachment; filename="f1_racing_video.mp4"');
  
  // Enviar archivo
  res.download(videoPath, 'f1_racing_video.mp4', (err) => {
    if (err) {
      console.error('Error al descargar video:', err);
      if (!res.headersSent) {
        res.status(500).send('Error al descargar el video');
      }
    } else {
      console.log('✅ Video descargado exitosamente');
    }
  });
});

/* GET descargar video con música */
router.get('/video-with-music', function(req, res) {
  const videoPath = path.join(OUTPUT_DIR, 'f1_racing_video_with_music.mp4');
  
  // Verificar si el archivo existe
  if (!fs.existsSync(videoPath)) {
    return res.status(404).send('Video con música no encontrado. Por favor, agrega música primero usando: node add-music.js /ruta/a/musica.mp3');
  }
  
  // Configurar headers para descarga
  res.setHeader('Content-Type', 'video/mp4');
  res.setHeader('Content-Disposition', 'attachment; filename="f1_racing_video_with_music.mp4"');
  
  // Enviar archivo
  res.download(videoPath, 'f1_racing_video_with_music.mp4', (err) => {
    if (err) {
      console.error('Error al descargar video con música:', err);
      if (!res.headersSent) {
        res.status(500).send('Error al descargar el video');
      }
    } else {
      console.log('✅ Video con música descargado exitosamente');
    }
  });
});

/* GET streaming del video (reproducir en navegador) */
router.get('/stream/video', function(req, res) {
  const videoPath = path.join(OUTPUT_DIR, 'f1_racing_video.mp4');
  
  if (!fs.existsSync(videoPath)) {
    return res.status(404).send('Video no encontrado');
  }
  
  const stat = fs.statSync(videoPath);
  const fileSize = stat.size;
  const range = req.headers.range;
  
  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
    const chunksize = (end - start) + 1;
    const file = fs.createReadStream(videoPath, {start, end});
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(206, head);
    file.pipe(res);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(200, head);
    fs.createReadStream(videoPath).pipe(res);
  }
});

/* GET streaming del video con música */
router.get('/stream/video-with-music', function(req, res) {
  const videoPath = path.join(OUTPUT_DIR, 'f1_racing_video_with_music.mp4');
  
  if (!fs.existsSync(videoPath)) {
    return res.status(404).send('Video con música no encontrado');
  }
  
  const stat = fs.statSync(videoPath);
  const fileSize = stat.size;
  const range = req.headers.range;
  
  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
    const chunksize = (end - start) + 1;
    const file = fs.createReadStream(videoPath, {start, end});
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(206, head);
    file.pipe(res);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(200, head);
    fs.createReadStream(videoPath).pipe(res);
  }
});

module.exports = router;
