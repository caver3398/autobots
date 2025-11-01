# 🎬 Cómo Descargar tu Video F1 con Audio

## ⚡ Método Rápido (3 pasos)

### 1️⃣ Inicia el servidor
```bash
npm start
```

### 2️⃣ Abre tu navegador
```
http://localhost:3000/download
```

### 3️⃣ Haz clic en "Descargar Video"
¡Listo! El video se descargará automáticamente.

---

## 🔗 Enlaces Directos de Descarga

Una vez que el servidor esté corriendo, puedes usar estos enlaces:

### 📹 Video sin música
```
http://localhost:3000/download/video
```

### 🎵 Video con música
```
http://localhost:3000/download/video-with-music
```

---

## 💡 Opciones Adicionales

### Ver el video en el navegador (streaming)
```
http://localhost:3000/download/stream/video
```

### Descargar desde terminal
```bash
# Con curl
curl -O http://localhost:3000/download/video

# Con wget
wget http://localhost:3000/download/video
```

---

## 🎵 Si aún no tienes música en el video

```bash
npm run add-music /ruta/a/tu/musica.mp3
```

Luego podrás descargar el video con música desde:
```
http://localhost:3000/download/video-with-music
```

---

## ✅ Verificar qué videos están disponibles

```bash
node test-download.js
```

Este comando te mostrará:
- ✅ Qué videos están listos para descargar
- 📊 Tamaño de cada video
- 🔗 URLs de descarga directa

---

## 📱 Compartir en Redes Sociales

Una vez descargado el video:

### Instagram Reels
1. Abre Instagram
2. Toca "+" → Reel
3. Sube el video descargado
4. ¡Publica!

### TikTok
1. Abre TikTok
2. Toca "+" → Subir
3. Selecciona el video
4. ¡Publica!

### YouTube Shorts
1. YouTube Studio → Subir
2. Selecciona el video
3. Marca como "Short"
4. ¡Publica!

---

## 🆘 ¿Problemas?

### "Video no encontrado"
Primero genera el video:
```bash
npm run generate-video
```

### "Cannot GET /download"
Asegúrate de que el servidor esté corriendo:
```bash
npm start
```

### Más ayuda
Lee el archivo completo: `DESCARGA_README.md`

---

## 🎉 ¡Eso es todo!

Tu video de F1 está listo para descargar y compartir en redes sociales.

**¡Disfruta y que se vuelva viral! 🏎️💨**
