// Datos del sistema
const sistemData = {
  zonas_pastoreo: [
    {
      id: "zona_1",
      nombre: "Sector Norte",
      estado: "critico",
      ndvi: 0.23,
      humedad_suelo: 15,
      temperatura: 28,
      precipitacion_ultimos_7_dias: 2,
      recomendacion: "Rotar ganado inmediatamente. Pasto insuficiente."
    },
    {
      id: "zona_2",
      nombre: "Sector Centro",
      estado: "regular",
      ndvi: 0.45,
      humedad_suelo: 35,
      temperatura: 24,
      precipitacion_ultimos_7_dias: 12,
      recomendacion: "Monitorear de cerca. Considerar rotación en 3-5 días."
    },
    {
      id: "zona_3",
      nombre: "Sector Sur",
      estado: "optimo",
      ndvi: 0.72,
      humedad_suelo: 55,
      temperatura: 22,
      precipitacion_ultimos_7_dias: 25,
      recomendacion: "Condiciones ideales para pastoreo. Aprovechar esta zona."
    }
  ],
  
  predicciones_clima: [
    {
      dia: "Hoy",
      temperatura_max: 26,
      temperatura_min: 14,
      precipitacion_prob: 20,
      viento: "15 km/h",
      estado: "Parcialmente nublado"
    },
    {
      dia: "Mañana",
      temperatura_max: 24,
      temperatura_min: 12,
      precipitacion_prob: 45,
      viento: "12 km/h",
      estado: "Probable lluvia"
    },
    {
      dia: "Pasado mañana",
      temperatura_max: 22,
      temperatura_min: 11,
      precipitacion_prob: 70,
      viento: "18 km/h",
      estado: "Lluvia"
    }
  ],
  
  tipos_reporte: [
    {
      id: "foto",
      nombre: "📷 Foto",
      descripcion: "Enviar foto del estado del pasto",
      campos: ["ubicacion", "descripcion", "foto"]
    },
    {
      id: "ubicacion",
      nombre: "📍 Ubicación",
      descripcion: "Reportar problema en ubicación específica",
      campos: ["coordenadas", "tipo_problema", "descripcion"]
    },
    {
      id: "problema",
      nombre: "⚠️ Problema",
      descripcion: "Reportar problema con ganado o infraestructura",
      campos: ["tipo_problema", "urgencia", "descripcion", "ubicacion"]
    },
    {
      id: "consejo",
      nombre: "💡 Solicitar Consejo",
      descripcion: "Pedir consejo técnico a especialista",
      campos: ["tema", "descripcion", "urgencia"]
    },
    {
      id: "emergencia",
      nombre: "🚨 Emergencia",
      descripcion: "Situación de emergencia que requiere atención inmediata",
      campos: ["tipo_emergencia", "ubicacion", "descripcion", "contacto"]
    }
  ],
  
  consejos_pastoreo: [
    {
      categoria: "Rotación",
      consejo: "Rote el ganado cada 21-28 días para permitir recuperación del pasto",
      temporada: "general"
    },
    {
      categoria: "Época Seca",
      consejo: "Durante sequía, reduzca carga animal y complemente con heno",
      temporada: "seca"
    },
    {
      categoria: "Época Lluviosa",
      consejo: "Evite sobrepastoreo en suelos húmedos para prevenir compactación",
      temporada: "lluviosa"
    },
    {
      categoria: "Nutrición",
      consejo: "Suplementar con sal mineral especialmente en época de lluvias",
      temporada: "general"
    }
  ],
  
  emergencias_comunes: [
    {
      tipo: "animal_herido",
      nombre: "Animal herido/enfermo",
      instrucciones: "Aisle el animal, contacte veterinario, mantenga en observación"
    },
    {
      tipo: "cerca_rota",
      nombre: "Cerca dañada",
      instrucciones: "Contenga animales, repare temporalmente, reporte ubicación exacta"
    },
    {
      tipo: "agua_contaminada",
      nombre: "Fuente de agua contaminada",
      instrucciones: "Evite que animales beban, busque fuente alternativa, reporte inmediato"
    }
  ]
};

// Estado actual del chat
let currentChatState = 'menu';
let currentFlow = null;
let selectedZone = null;

// Referencias DOM
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const modalOverlay = document.getElementById('modal-overlay');
const modalTitle = document.getElementById('modal-title');
const modalContent = document.getElementById('modal-content');

// Funciones de navegación principal
function showWhatsApp() {
  document.getElementById('whatsapp-interface').style.display = 'block';
  document.getElementById('dashboard-interface').style.display = 'none';
  resetChat();
}

function showDashboard() {
  document.getElementById('whatsapp-interface').style.display = 'none';
  document.getElementById('dashboard-interface').style.display = 'block';
  loadDashboardData();
}

// Funciones del chat de WhatsApp
function addMessage(content, isUser = false, showTime = true) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  contentDiv.innerHTML = content;
  
  messageDiv.appendChild(contentDiv);
  
  if (showTime) {
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    messageDiv.appendChild(timeDiv);
  }
  
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showMainMenu() {
  currentChatState = 'menu';
  chatInput.innerHTML = `
    <div class="main-menu">
      <button class="menu-btn" onclick="consultarEstadoPastos()">🌱 Estado Pastos</button>
      <button class="menu-btn" onclick="enviarReporte()">📝 Enviar Reporte</button>
      <button class="menu-btn" onclick="consultarClima()">🌤️ Agua/Clima</button>
      <button class="menu-btn" onclick="solicitarConsejos()">💡 Consejos</button>
      <button class="menu-btn" onclick="reportarEmergencia()">🚨 Emergencia</button>
    </div>
  `;
}

function resetChat() {
  chatMessages.innerHTML = `
    <div class="message bot-message">
      <div class="message-content">
        ¡Hola! 👋 Soy tu asistente de pastoreo inteligente.
        <br><br>¿En qué te puedo ayudar hoy?
      </div>
      <div class="message-time">10:00</div>
    </div>
  `;
  showMainMenu();
}

// Flujo: Consultar Estado de Pastos
function consultarEstadoPastos() {
  addMessage('Consultar estado de pastos', true);
  
  setTimeout(() => {
    addMessage('Perfecto! Selecciona la zona que quieres consultar:');
    
    let buttonsHTML = '<div class="main-menu">';
    sistemData.zonas_pastoreo.forEach(zona => {
      const statusColor = zona.estado === 'critico' ? '🔴' : zona.estado === 'regular' ? '🟡' : '🟢';
      buttonsHTML += `<button class="menu-btn" onclick="mostrarEstadoZona('${zona.id}')">${statusColor} ${zona.nombre}</button>`;
    });
    buttonsHTML += '<button class="menu-btn" onclick="showMainMenu()">⬅️ Volver</button></div>';
    
    chatInput.innerHTML = buttonsHTML;
  }, 1000);
}

function mostrarEstadoZona(zonaId) {
  const zona = sistemData.zonas_pastoreo.find(z => z.id === zonaId);
  addMessage(`Consultar ${zona.nombre}`, true);
  
  setTimeout(() => {
    const statusEmoji = zona.estado === 'critico' ? '🔴' : zona.estado === 'regular' ? '🟡' : '🟢';
    const statusText = zona.estado === 'critico' ? 'CRÍTICO' : zona.estado === 'regular' ? 'REGULAR' : 'ÓPTIMO';
    
    const responseHTML = `
      <strong>${statusEmoji} ${zona.nombre} - Estado ${statusText}</strong><br><br>
      
      📊 <strong>Métricas actuales:</strong><br>
      • NDVI: ${zona.ndvi}<br>
      • Humedad del suelo: ${zona.humedad_suelo}%<br>
      • Temperatura: ${zona.temperatura}°C<br>
      • Lluvia últimos 7 días: ${zona.precipitacion_ultimos_7_dias}mm<br><br>
      
      💡 <strong>Recomendación:</strong><br>
      ${zona.recomendacion}
    `;
    
    addMessage(responseHTML);
    
    setTimeout(() => {
      chatInput.innerHTML = `
        <div class="main-menu">
          <button class="menu-btn" onclick="consultarEstadoPastos()">🔄 Otra Zona</button>
          <button class="menu-btn" onclick="showMainMenu()">⬅️ Menú Principal</button>
        </div>
      `;
    }, 2000);
  }, 1500);
}

// Flujo: Enviar Reporte
function enviarReporte() {
  addMessage('Enviar reporte', true);
  
  setTimeout(() => {
    addMessage('¿Qué tipo de reporte quieres enviar?');
    
    let buttonsHTML = '<div class="main-menu">';
    sistemData.tipos_reporte.forEach(tipo => {
      buttonsHTML += `<button class="menu-btn" onclick="seleccionarTipoReporte('${tipo.id}')">${tipo.nombre}</button>`;
    });
    buttonsHTML += '<button class="menu-btn" onclick="showMainMenu()">⬅️ Volver</button></div>';
    
    chatInput.innerHTML = buttonsHTML;
  }, 1000);
}

function seleccionarTipoReporte(tipoId) {
  const tipo = sistemData.tipos_reporte.find(t => t.id === tipoId);
  addMessage(tipo.nombre, true);
  
  setTimeout(() => {
    addMessage(`Perfecto! Vamos a crear un reporte de tipo: <strong>${tipo.descripcion}</strong><br><br>Por favor completa la información requerida:`);
    
    // Mostrar formulario simplificado
    setTimeout(() => {
      mostrarFormularioReporte(tipo);
    }, 1000);
  }, 1000);
}

function mostrarFormularioReporte(tipo) {
  const formHTML = `
    <div style="text-align: left;">
      <div class="form-group">
        <label class="form-label">Descripción del problema:</label>
        <textarea class="form-control" id="reporte-descripcion" rows="3" placeholder="Describe lo que observaste..."></textarea>
      </div>
      <div class="form-group">
        <label class="form-label">Ubicación:</label>
        <input type="text" class="form-control" id="reporte-ubicacion" placeholder="Ej: Cerca del abrevadero sur">
      </div>
      <div class="form-group">
        <label class="form-label">Nivel de urgencia:</label>
        <select class="form-control" id="reporte-urgencia">
          <option value="baja">Baja</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
        </select>
      </div>
      <div style="text-align: center; margin-top: 20px;">
        <button class="btn btn--primary" onclick="enviarReporteCompleto('${tipo.id}')">📤 Enviar Reporte</button>
        <button class="btn btn--secondary" onclick="showMainMenu()" style="margin-left: 10px;">❌ Cancelar</button>
      </div>
    </div>
  `;
  
  chatInput.innerHTML = formHTML;
}

function enviarReporteCompleto(tipoId) {
  const descripcion = document.getElementById('reporte-descripcion').value;
  const ubicacion = document.getElementById('reporte-ubicacion').value;
  const urgencia = document.getElementById('reporte-urgencia').value;
  
  if (!descripcion || !ubicacion) {
    alert('Por favor completa todos los campos obligatorios');
    return;
  }
  
  addMessage(`✅ Reporte enviado exitosamente!<br><br>📋 <strong>Resumen:</strong><br>• Descripción: ${descripcion}<br>• Ubicación: ${ubicacion}<br>• Urgencia: ${urgencia}<br><br>Un especialista revisará tu reporte y te contactará si es necesario.`);
  
  setTimeout(() => {
    showMainMenu();
  }, 3000);
}

// Flujo: Consultar Clima
function consultarClima() {
  addMessage('Consultar clima y agua', true);
  
  setTimeout(() => {
    addMessage('📡 Consultando estaciones meteorológicas y modelo predictivo...');
    
    setTimeout(() => {
      let climaHTML = '🌤️ <strong>Predicción Climática</strong><br><br>';
      
      sistemData.predicciones_clima.forEach(pred => {
        const alertIcon = pred.precipitacion_prob > 60 ? '⚠️' : pred.precipitacion_prob > 30 ? '⚡' : '☀️';
        climaHTML += `${alertIcon} <strong>${pred.dia}:</strong><br>`;
        climaHTML += `• ${pred.estado}<br>`;
        climaHTML += `• Temp: ${pred.temperatura_min}°C - ${pred.temperatura_max}°C<br>`;
        climaHTML += `• Probabilidad lluvia: ${pred.precipitacion_prob}%<br>`;
        climaHTML += `• Viento: ${pred.viento}<br><br>`;
      });
      
      climaHTML += '💧 <strong>Recomendaciones de Agua:</strong><br>';
      climaHTML += '• Revise niveles de abrevaderos<br>';
      climaHTML += '• Mantenga fuentes alternativas disponibles<br>';
      climaHTML += '• Considere suplementación en época seca';
      
      addMessage(climaHTML);
      
      setTimeout(() => {
        showMainMenu();
      }, 4000);
    }, 2000);
  }, 1000);
}

// Flujo: Consejos
function solicitarConsejos() {
  addMessage('Solicitar consejos', true);
  
  setTimeout(() => {
    addMessage('💡 Aquí tienes algunos consejos útiles para el manejo de pastoreo:');
    
    setTimeout(() => {
      let consejosHTML = '';
      sistemData.consejos_pastoreo.forEach((consejo, index) => {
        consejosHTML += `<strong>${index + 1}. ${consejo.categoria}:</strong><br>`;
        consejosHTML += `${consejo.consejo}<br><br>`;
      });
      
      consejosHTML += '¿Necesitas consejos más específicos? Puedes enviar un reporte solicitando asesoría personalizada.';
      
      addMessage(consejosHTML);
      
      setTimeout(() => {
        chatInput.innerHTML = `
          <div class="main-menu">
            <button class="menu-btn" onclick="enviarReporte()">📝 Solicitar Asesoría</button>
            <button class="menu-btn" onclick="showMainMenu()">⬅️ Menú Principal</button>
          </div>
        `;
      }, 3000);
    }, 1500);
  }, 1000);
}

// Flujo: Emergencia
function reportarEmergencia() {
  addMessage('🚨 EMERGENCIA', true);
  
  setTimeout(() => {
    addMessage('🚨 <strong>MODO EMERGENCIA ACTIVADO</strong><br><br>Selecciona el tipo de emergencia:');
    
    let buttonsHTML = '<div class="main-menu">';
    sistemData.emergencias_comunes.forEach(emergencia => {
      buttonsHTML += `<button class="menu-btn" onclick="procesarEmergencia('${emergencia.tipo}')" style="background: #ff5555; color: white;">${emergencia.nombre}</button>`;
    });
    buttonsHTML += '<button class="menu-btn" onclick="showMainMenu()">❌ Cancelar</button></div>';
    
    chatInput.innerHTML = buttonsHTML;
  }, 1000);
}

function procesarEmergencia(tipoEmergencia) {
  const emergencia = sistemData.emergencias_comunes.find(e => e.tipo === tipoEmergencia);
  addMessage(emergencia.nombre, true);
  
  setTimeout(() => {
    addMessage(`🚨 <strong>EMERGENCIA: ${emergencia.nombre}</strong><br><br>📋 <strong>Instrucciones inmediatas:</strong><br>${emergencia.instrucciones}<br><br>📞 <strong>Especialistas notificados</strong><br>Se ha enviado alerta a los técnicos disponibles.<br><br>⏰ Un especialista te contactará en los próximos 15 minutos.`);
    
    setTimeout(() => {
      addMessage('📞 <strong>Contacto de emergencia establecido</strong><br><br>El técnico Juan Pérez está en camino.<br>Teléfono de contacto: +57 300 123 4567<br><br>Mantente en la zona y sigue las instrucciones proporcionadas.');
      
      setTimeout(() => {
        showMainMenu();
      }, 4000);
    }, 3000);
  }, 1000);
}

// Funciones del Dashboard
function loadDashboardData() {
  loadZonesData();
  loadReportsData();
}

function loadZonesData() {
  const zonesGrid = document.getElementById('zones-grid');
  zonesGrid.innerHTML = '';
  
  sistemData.zonas_pastoreo.forEach(zona => {
    const zoneCard = document.createElement('div');
    zoneCard.className = 'zone-card';
    zoneCard.innerHTML = `
      <div class="zone-status ${zona.estado}"></div>
      <div class="zone-title">${zona.nombre}</div>
      <div class="zone-metrics">
        <div class="metric">NDVI: <strong>${zona.ndvi}</strong></div>
        <div class="metric">Humedad: <strong>${zona.humedad_suelo}%</strong></div>
        <div class="metric">Temp: <strong>${zona.temperatura}°C</strong></div>
        <div class="metric">Lluvia 7d: <strong>${zona.precipitacion_ultimos_7_dias}mm</strong></div>
      </div>
      <div class="zone-recommendation">
        ${zona.recomendacion}
      </div>
    `;
    zonesGrid.appendChild(zoneCard);
  });
}

function loadReportsData() {
  const reportsList = document.getElementById('reports-list');
  const sampleReports = [
    { tipo: 'Foto de pasto', tiempo: 'Hace 2 horas', status: 'pendiente' },
    { tipo: 'Problema cerca', tiempo: 'Hace 4 horas', status: 'validado' },
    { tipo: 'Solicitud consejo', tiempo: 'Hace 6 horas', status: 'pendiente' },
    { tipo: 'Animal herido', tiempo: 'Ayer', status: 'validado' },
    { tipo: 'Ubicación problema', tiempo: 'Hace 2 días', status: 'validado' }
  ];
  
  reportsList.innerHTML = '';
  
  sampleReports.forEach(report => {
    const reportItem = document.createElement('div');
    reportItem.className = 'report-item';
    reportItem.innerHTML = `
      <div class="report-info">
        <div class="report-type">${report.tipo}</div>
        <div class="report-time">${report.tiempo}</div>
      </div>
      <div class="report-status ${report.status}">${report.status}</div>
    `;
    reportsList.appendChild(reportItem);
  });
}

// Funciones de acciones del dashboard
function retrainModel() {
  showModal('Reentrenar Modelo', `
    <p>¿Estás seguro de que quieres reentrenar el modelo XGBoost?</p>
    <p><strong>Datos disponibles:</strong> 15,420 registros</p>
    <p><strong>Tiempo estimado:</strong> 45 minutos</p>
    <div style="text-align: center; margin-top: 20px;">
      <button class="btn btn--primary" onclick="startRetraining()">🚀 Iniciar Reentrenamiento</button>
      <button class="btn btn--secondary" onclick="closeModal()" style="margin-left: 10px;">Cancelar</button>
    </div>
  `);
}

function startRetraining() {
  closeModal();
  alert('🚀 Reentrenamiento iniciado. Recibirás una notificación cuando termine.');
}

function validateReports() {
  showModal('Validar Reportes', `
    <p>Reportes pendientes de validación: <strong>7</strong></p>
    <div style="margin: 20px 0;">
      <div style="padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px;">
        <strong>📷 Foto de pasto deteriorado</strong><br>
        <small>Enviado hace 2 horas por Juan Rodríguez</small><br>
        <button class="btn btn--primary" style="margin-top: 8px; margin-right: 8px;">✅ Validar</button>
        <button class="btn btn--secondary" style="margin-top: 8px;">❌ Rechazar</button>
      </div>
      <div style="padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px;">
        <strong>💡 Solicitud de consejo</strong><br>
        <small>Enviado hace 6 horas por María López</small><br>
        <button class="btn btn--primary" style="margin-top: 8px; margin-right: 8px;">✅ Responder</button>
        <button class="btn btn--secondary" style="margin-top: 8px;">⏰ Más tarde</button>
      </div>
    </div>
    <div style="text-align: center;">
      <button class="btn btn--secondary" onclick="closeModal()">Cerrar</button>
    </div>
  `);
}

function updateAdvice() {
  showModal('Actualizar Base de Consejos', `
    <p>Gestiona la base de conocimientos de consejos de pastoreo:</p>
    <div class="form-group">
      <label class="form-label">Categoría:</label>
      <select class="form-control">
        <option>Rotación</option>
        <option>Nutrición</option>
        <option>Época Seca</option>
        <option>Época Lluviosa</option>
        <option>Emergencias</option>
      </select>
    </div>
    <div class="form-group">
      <label class="form-label">Nuevo consejo:</label>
      <textarea class="form-control" rows="3" placeholder="Escribe el consejo aquí..."></textarea>
    </div>
    <div style="text-align: center; margin-top: 20px;">
      <button class="btn btn--primary" onclick="addAdvice()">➕ Agregar Consejo</button>
      <button class="btn btn--secondary" onclick="closeModal()" style="margin-left: 10px;">Cancelar</button>
    </div>
  `);
}

function addAdvice() {
  closeModal();
  alert('✅ Consejo agregado exitosamente a la base de conocimientos.');
}

function exportData() {
  showModal('Exportar Datos', `
    <p>Selecciona los datos que quieres exportar:</p>
    <div style="margin: 20px 0;">
      <label style="display: block; margin-bottom: 10px;">
        <input type="checkbox" checked> Datos de zonas de pastoreo
      </label>
      <label style="display: block; margin-bottom: 10px;">
        <input type="checkbox" checked> Reportes de usuarios
      </label>
      <label style="display: block; margin-bottom: 10px;">
        <input type="checkbox"> Métricas del modelo
      </label>
      <label style="display: block; margin-bottom: 10px;">
        <input type="checkbox"> Datos climáticos
      </label>
    </div>
    <div style="text-align: center;">
      <button class="btn btn--primary" onclick="startExport()">📊 Exportar CSV</button>
      <button class="btn btn--secondary" onclick="closeModal()" style="margin-left: 10px;">Cancelar</button>
    </div>
  `);
}

function startExport() {
  closeModal();
  alert('📊 Exportación iniciada. El archivo se descargará automáticamente.');
}

// Funciones de modal
function showModal(title, content) {
  modalTitle.textContent = title;
  modalContent.innerHTML = content;
  modalOverlay.style.display = 'flex';
}

function closeModal() {
  modalOverlay.style.display = 'none';
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
  showWhatsApp();
});