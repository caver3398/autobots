const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');

// Cargar configuración de ventas
const configPath = path.join(__dirname, '../config/ventas-config.json');

/* GET página de ventas */
router.get('/', function(req, res, next) {
  try {
    // Leer el archivo de configuración
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    // Renderizar la vista con la configuración
    res.render('ventas', { 
      title: 'Página de Ventas',
      config: config
    });
  } catch (error) {
    console.error('Error al cargar configuración de ventas:', error);
    res.status(500).render('error', { 
      message: 'Error al cargar la página de ventas',
      error: error
    });
  }
});

/* POST formulario de contacto */
router.post('/contacto', function(req, res) {
  const { nombre, email, telefono, mensaje } = req.body;
  
  // Aquí puedes agregar la lógica para enviar emails o guardar en base de datos
  console.log('Nuevo contacto recibido:');
  console.log('Nombre:', nombre);
  console.log('Email:', email);
  console.log('Teléfono:', telefono);
  console.log('Mensaje:', mensaje);
  
  // Por ahora, solo enviamos una respuesta JSON
  res.json({ 
    success: true, 
    message: 'Gracias por contactarnos. Te responderemos pronto.' 
  });
});

module.exports = router;
