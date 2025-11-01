#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🏎️  EJEMPLOS DE DESCARGA DE VIDEOS F1
# ═══════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║   🏎️  EJEMPLOS DE DESCARGA DE VIDEOS F1                       ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════
# MÉTODO 1: Descargar con curl
# ═══════════════════════════════════════════════════════════════

echo "📥 MÉTODO 1: Descargar con curl"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Video sin música:"
echo "curl -o f1_video.mp4 http://localhost:3000/download/video"
echo ""
echo "# Video con música:"
echo "curl -o f1_video_con_musica.mp4 http://localhost:3000/download/video-with-music"
echo ""
echo "# Con barra de progreso:"
echo "curl -# -o f1_video.mp4 http://localhost:3000/download/video"
echo ""

# ═══════════════════════════════════════════════════════════════
# MÉTODO 2: Descargar con wget
# ═══════════════════════════════════════════════════════════════

echo "📥 MÉTODO 2: Descargar con wget"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Video sin música:"
echo "wget http://localhost:3000/download/video"
echo ""
echo "# Video con música:"
echo "wget http://localhost:3000/download/video-with-music"
echo ""
echo "# Con nombre personalizado:"
echo "wget -O mi_video_f1.mp4 http://localhost:3000/download/video"
echo ""

# ═══════════════════════════════════════════════════════════════
# MÉTODO 3: Streaming en navegador
# ═══════════════════════════════════════════════════════════════

echo "▶️  MÉTODO 3: Ver en navegador (streaming)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Abre en tu navegador:"
echo "http://localhost:3000/download/stream/video"
echo ""
echo "# O con xdg-open (Linux):"
echo "xdg-open http://localhost:3000/download/stream/video"
echo ""
echo "# O con open (macOS):"
echo "open http://localhost:3000/download/stream/video"
echo ""

# ═══════════════════════════════════════════════════════════════
# MÉTODO 4: Interfaz web
# ═══════════════════════════════════════════════════════════════

echo "🌐 MÉTODO 4: Interfaz web"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Abre en tu navegador:"
echo "http://localhost:3000/download"
echo ""
echo "# O con comando:"
echo "xdg-open http://localhost:3000/download  # Linux"
echo "open http://localhost:3000/download      # macOS"
echo "start http://localhost:3000/download     # Windows"
echo ""

# ═══════════════════════════════════════════════════════════════
# MÉTODO 5: Descargar múltiples videos
# ═══════════════════════════════════════════════════════════════

echo "📦 MÉTODO 5: Descargar múltiples videos"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Descargar ambos videos:"
echo "curl -o f1_video.mp4 http://localhost:3000/download/video && \\"
echo "curl -o f1_video_con_musica.mp4 http://localhost:3000/download/video-with-music"
echo ""

# ═══════════════════════════════════════════════════════════════
# MÉTODO 6: Verificar antes de descargar
# ═══════════════════════════════════════════════════════════════

echo "🔍 MÉTODO 6: Verificar antes de descargar"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Ver información del archivo:"
echo "curl -I http://localhost:3000/download/video"
echo ""
echo "# Ver tamaño del archivo:"
echo "curl -sI http://localhost:3000/download/video | grep -i content-length"
echo ""

# ═══════════════════════════════════════════════════════════════
# EJEMPLOS AVANZADOS
# ═══════════════════════════════════════════════════════════════

echo "🚀 EJEMPLOS AVANZADOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Descargar con reintentos automáticos:"
echo "curl --retry 3 --retry-delay 2 -o f1_video.mp4 http://localhost:3000/download/video"
echo ""
echo "# Descargar con límite de velocidad:"
echo "curl --limit-rate 1M -o f1_video.mp4 http://localhost:3000/download/video"
echo ""
echo "# Descargar y continuar si se interrumpe:"
echo "curl -C - -o f1_video.mp4 http://localhost:3000/download/video"
echo ""
echo "# Descargar en segundo plano:"
echo "curl -o f1_video.mp4 http://localhost:3000/download/video &"
echo ""

# ═══════════════════════════════════════════════════════════════
# SCRIPT DE DESCARGA AUTOMÁTICA
# ═══════════════════════════════════════════════════════════════

echo "🤖 SCRIPT DE DESCARGA AUTOMÁTICA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Guarda esto en un archivo 'descargar.sh':"
echo ""
cat << 'SCRIPT'
#!/bin/bash
echo "🏎️  Descargando videos F1..."
curl -# -o f1_video.mp4 http://localhost:3000/download/video
if [ $? -eq 0 ]; then
    echo "✅ Video descargado: f1_video.mp4"
else
    echo "❌ Error al descargar video"
fi
SCRIPT
echo ""
echo "# Luego ejecuta:"
echo "chmod +x descargar.sh"
echo "./descargar.sh"
echo ""

# ═══════════════════════════════════════════════════════════════
# INTEGRACIÓN CON OTRAS HERRAMIENTAS
# ═══════════════════════════════════════════════════════════════

echo "🔧 INTEGRACIÓN CON OTRAS HERRAMIENTAS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Descargar y reproducir con VLC:"
echo "curl -s http://localhost:3000/download/video | vlc -"
echo ""
echo "# Descargar y obtener información con ffprobe:"
echo "curl -s http://localhost:3000/download/video | ffprobe -"
echo ""
echo "# Descargar y subir a otro servidor:"
echo "curl http://localhost:3000/download/video | \\"
echo "  curl -X POST -F 'video=@-' https://tu-servidor.com/upload"
echo ""

# ═══════════════════════════════════════════════════════════════
# NOTAS IMPORTANTES
# ═══════════════════════════════════════════════════════════════

echo "📝 NOTAS IMPORTANTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Asegúrate de que el servidor esté corriendo:"
echo "   npm start"
echo ""
echo "2. Verifica que el video exista:"
echo "   npm run check-downloads"
echo ""
echo "3. Si el video no existe, genera uno:"
echo "   npm run generate-video"
echo ""
echo "4. Para agregar música:"
echo "   npm run add-music /ruta/a/musica.mp3"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║   ✅ ¡Listo para descargar tus videos F1!                     ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
