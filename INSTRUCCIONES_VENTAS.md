# 📄 Página de Ventas - Guía de Uso

## 🎯 ¿Qué se ha creado?

Se ha implementado una **página de ventas profesional y moderna** completamente funcional y fácil de personalizar. La página incluye:

- ✅ Sección Hero (Encabezado principal)
- ✅ Características del producto/servicio
- ✅ Planes de precios
- ✅ Testimonios de clientes
- ✅ Llamada a la acción (CTA)
- ✅ Formulario de contacto funcional
- ✅ Diseño responsive (móvil, tablet, desktop)
- ✅ Animaciones suaves
- ✅ Estilos modernos

## 🚀 Cómo acceder a la página

1. Inicia el servidor:
   ```bash
   npm start
   ```

2. Abre tu navegador y visita:
   ```
   http://localhost:3000/ventas
   ```

## ✏️ Cómo modificar el contenido (MUY FÁCIL)

**¡Esta es la parte más importante!** Para cambiar TODO el contenido de la página, solo necesitas editar UN archivo:

### Archivo a modificar:
```
config/ventas-config.json
```

### ¿Qué puedes cambiar?

#### 1. **Sección Hero (Encabezado)**
```json
"hero": {
  "titulo": "Tu título aquí",
  "subtitulo": "Tu subtítulo aquí",
  "botonTexto": "Texto del botón",
  "botonLink": "#contacto"
}
```

#### 2. **Características**
Puedes agregar, eliminar o modificar características:
```json
"caracteristicas": [
  {
    "icono": "⚡",  // Cambia el emoji
    "titulo": "Título de la característica",
    "descripcion": "Descripción detallada"
  }
]
```

#### 3. **Planes de Precios**
```json
"planes": [
  {
    "nombre": "Nombre del Plan",
    "precio": "$99",
    "periodo": "/mes",
    "caracteristicas": [
      "Característica 1",
      "Característica 2"
    ],
    "destacado": true,  // true para resaltar el plan
    "botonTexto": "Elegir Plan"
  }
]
```

#### 4. **Testimonios**
```json
"testimonios": [
  {
    "nombre": "Nombre del Cliente",
    "empresa": "Nombre de la Empresa",
    "texto": "El testimonio aquí",
    "avatar": "👨‍💼"  // Cambia el emoji
  }
]
```

#### 5. **Formulario de Contacto**
```json
"contacto": {
  "titulo": "Título del formulario",
  "subtitulo": "Subtítulo",
  "campos": {
    "nombre": "Etiqueta del campo nombre",
    "email": "Etiqueta del campo email",
    "telefono": "Etiqueta del campo teléfono",
    "mensaje": "Etiqueta del campo mensaje"
  },
  "botonEnviar": "Texto del botón"
}
```

## 🎨 Cómo cambiar los colores

Si quieres cambiar los colores de la página, edita el archivo:
```
public/stylesheets/ventas.css
```

Al inicio del archivo encontrarás las variables de color:
```css
:root {
  --primary-color: #6366f1;      /* Color principal */
  --primary-dark: #4f46e5;       /* Color principal oscuro */
  --secondary-color: #8b5cf6;    /* Color secundario */
  --text-dark: #1f2937;          /* Color del texto */
  --text-light: #6b7280;         /* Color del texto claro */
}
```

## 📧 Formulario de Contacto

El formulario ya está funcional. Cuando alguien envía el formulario:

1. Los datos se envían a `/ventas/contacto`
2. Por ahora, los datos se muestran en la consola del servidor
3. El usuario recibe un mensaje de confirmación

### Para conectar con email o base de datos:

Edita el archivo `routes/ventas.js` en la sección `POST /contacto`:

```javascript
router.post('/contacto', function(req, res) {
  const { nombre, email, telefono, mensaje } = req.body;
  
  // AQUÍ puedes agregar:
  // - Envío de emails (con nodemailer)
  // - Guardar en base de datos
  // - Integrar con CRM
  // - Enviar a Slack, Discord, etc.
  
  res.json({ 
    success: true, 
    message: 'Gracias por contactarnos.' 
  });
});
```

## 📱 Responsive Design

La página se adapta automáticamente a:
- 📱 Móviles (menos de 480px)
- 📱 Tablets (menos de 768px)
- 💻 Desktop (más de 768px)

## 🔧 Archivos Creados

```
/vercel/sandbox/
├── config/
│   └── ventas-config.json          ← EDITA ESTE para cambiar contenido
├── routes/
│   └── ventas.js                   ← Lógica del servidor
├── views/
│   └── ventas.pug                  ← Plantilla HTML
├── public/
│   └── stylesheets/
│       └── ventas.css              ← Estilos (colores, diseño)
└── INSTRUCCIONES_VENTAS.md         ← Este archivo
```

## 💡 Consejos

1. **Siempre guarda los cambios** en `ventas-config.json` antes de recargar la página
2. **Usa emojis** para los iconos (son universales y no requieren librerías)
3. **Prueba en móvil** abriendo desde tu teléfono: `http://TU_IP:3000/ventas`
4. **Haz copias de seguridad** del archivo JSON antes de hacer cambios grandes

## 🆘 Solución de Problemas

### La página no carga
- Verifica que el servidor esté corriendo: `npm start`
- Revisa que no haya errores en la consola

### Los cambios no se ven
- Recarga la página con Ctrl+F5 (o Cmd+Shift+R en Mac)
- Verifica que el archivo JSON tenga sintaxis correcta

### Error en el JSON
- Usa un validador JSON online: https://jsonlint.com/
- Asegúrate de que todas las comillas sean dobles `"`
- Verifica que no falten comas entre elementos

## 📞 Próximos Pasos

1. **Personaliza el contenido** editando `ventas-config.json`
2. **Cambia los colores** si lo deseas en `ventas.css`
3. **Conecta el formulario** a tu email o base de datos
4. **Agrega Google Analytics** para seguimiento
5. **Integra pasarelas de pago** si vendes productos

---

¡Listo! Ahora tienes una página de ventas profesional y fácil de modificar. 🎉
