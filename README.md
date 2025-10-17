# 🌿 OCKO: Bot de WhatsApp Modular para Monitoreo y Gestión de Pastizales

## 📋 Descripción General

Ocko es un chatbot modular diseñado para ofrecer inteligencia de pastizales en tiempo real a través de WhatsApp. Utiliza un **Clasificador Random Forest (Machine Learning)** para predecir el estado de salud del pastizal mediante un sistema de semáforo y opera a través de dos canales IVR completamente separados: **Comuneros** y **Especialistas**.

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
/ocko_whatsapp_project
├── /data
│   ├── /raw                        # Datos originales de campo (CSVs)
│   └── /processed                  # Indicadores consolidados (ML_Grassland_Indicators.csv)
│
├── /models
│   ├── random_forest_model.pkl     # Modelo ML entrenado
│   └── label_encoder.pkl           # Codificador de clases (Green/Yellow/Red)
│
├── /src                            # Código fuente principal
│   ├── /flows                      # Lógica de Flujo por Canal (IVR)
│   │   ├── comunero_ivr.py         # IVR Comunero: Predicción ML, Reportes
│   │   └── especialista_ivr.py     # IVR Especialista: Alertas, Validación
│   │
│   ├── /utils                      # Funciones de Soporte
│   │   ├── api_handler.py          # Simulación del envío a la API de Meta
│   │   ├── data_loader.py          # Carga centralizada y lazy de artefactos ML
│   │   └── data_processor.py       # Entrenamiento del modelo ML
│   │
│   ├── main_webhook.py             # PUNTO DE ENTRADA: Enrutamiento de mensajes
│   └── config.py                   # Constantes y configuración global
│
├── .env                            # Variables de entorno (Tokens, URLs, Teléfonos)
├── requirements.txt                # Dependencias de Python
└── README.md                       # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de WhatsApp Business API
- Acceso a Meta Graph API

### Paso 1: Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd ocko_whatsapp_project
```

### Paso 2: Crear Entorno Virtual

```bash
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```bash
# Credenciales de WhatsApp Business API
WHATSAPP_API_TOKEN="TU_TOKEN_DE_ACCESO_DE_META"
WHATSAPP_API_URL="https://graph.whatsapp.com/v17.0/TU_PHONE_ID/messages"

# Números de teléfono de prueba (incluir código de país)
COMUNERO_PHONE="51987654321"
ESPECIALISTA_PHONE="51912345678"
```

### Paso 5: Preparar los Datos

Coloca tus archivos CSV originales en el directorio `data/raw/` con los siguientes nombres:

- `Data_DispoGrass.csv`
- `Data_PlantVigor.csv`
- (Otros archivos de datos necesarios)

---

## 🤖 Uso del Sistema

### Entrenar el Modelo ML

Antes de ejecutar el bot por primera vez, debes entrenar el modelo de Machine Learning:

```bash
python src/utils/data_processor.py
```

Este script realiza las siguientes operaciones:

- Carga y procesa los datos crudos
- Aplica imputación robusta para valores faltantes
- Entrena el clasificador Random Forest
- Genera los archivos `random_forest_model.pkl` y `label_encoder.pkl`
- Crea el archivo consolidado `ML_Grassland_Indicators.csv`

### Iniciar el Bot

**⚠️ IMPORTANTE:** Siempre ejecuta el bot desde la raíz del proyecto usando el comando de módulo:

```bash
python -m src.main_webhook
```

El sistema iniciará y cargará los artefactos ML mediante lazy loading, optimizando el uso de memoria.

---

## 📱 Canales y Funcionalidades

### Canal: Comuneros

Diseñado para usuarios de campo que monitorean los pastizales.

| Opción | Funcionalidad | Descripción |
|--------|---------------|-------------|
| **1** | Estado de Pastos | Utiliza el modelo ML para predecir el estado del pastizal (Semáforo: Verde/Amarillo/Rojo) |
| **2** | Consultar Historial | Muestra el historial de reportes y mediciones |
| **3** | Enviar Reporte | Flujo secuencial guiado: Foto → Observación → Confirmación |
| **4** | Ayuda | Información sobre cómo usar el bot |

**Características especiales:**

- **Predicción ML en tiempo real:** Análisis inmediato del estado del pastizal
- **Gestión de estado conversacional:** Mantiene el contexto durante reportes secuenciales
- **Interfaz simplificada:** Diseñada para facilitar el uso en campo

### Canal: Especialistas

Diseñado para técnicos y expertos en gestión de pastizales.

| Opción | Funcionalidad | Descripción |
|--------|---------------|-------------|
| **1** | Ver Alertas | Filtra y reporta zonas críticas del archivo `ML_Grassland_Indicators.csv` |
| **2** | Análisis Avanzado | Estadísticas detalladas y tendencias |
| **3** | Configuración | Ajustes del sistema de alertas |
| **4** | Validar Modelo | Reporta el estado del modelo ML (desbalance de clases, precisión, etc.) |

**Características especiales:**

- **Gestión de datos avanzada:** Acceso directo a indicadores procesados
- **Validación de modelo:** Herramientas para evaluar la calidad del ML
- **Alertas inteligentes:** Sistema de notificación basado en umbrales

---

## 🧠 Sistema de Machine Learning

### Modelo: Random Forest Classifier

El sistema utiliza un clasificador Random Forest para predecir el estado de salud del pastizal en tres categorías:

- 🟢 **Verde:** Pastizal saludable
- 🟡 **Amarillo:** Pastizal en estado de alerta
- 🔴 **Rojo:** Pastizal en condición crítica

### Características del Modelo

- **Imputación robusta:** Manejo inteligente de valores faltantes
- **Codificación de etiquetas:** Transformación consistente de clases
- **Lazy Loading:** Carga única y centralizada de artefactos
- **Persistencia:** Modelos guardados en formato pickle para rápida recuperación

### Flujo de Datos ML

```
Datos Crudos (CSV) 
    ↓
data_processor.py
    ↓
Modelo Entrenado + Indicadores Procesados
    ↓
data_loader.py (Lazy Loading)
    ↓
Predicciones en Tiempo Real
```

---

## 🔧 Arquitectura Técnica

### Componentes Principales

#### 1. `main_webhook.py`

- **Rol:** Punto de entrada del sistema
- **Funciones:**
  - Enrutamiento de mensajes según número de origen
  - Carga única de artefactos ML
  - Delegación a flujos específicos (Comunero/Especialista)

#### 2. `flows/comunero_ivr.py`

- **Rol:** Lógica IVR para comuneros
- **Funciones:**
  - Manejo de opciones de menú
  - Integración con predictor ML
  - Gestión de flujos secuenciales (reportes)

#### 3. `flows/especialista_ivr.py`

- **Rol:** Lógica IVR para especialistas
- **Funciones:**
  - Sistema de alertas avanzado
  - Validación de modelo ML
  - Análisis de datos consolidados

#### 4. `utils/data_loader.py`

- **Rol:** Gestión centralizada de recursos ML
- **Funciones:**
  - Lazy loading de modelos
  - Prevención de ciclos de importación
  - Optimización de memoria

#### 5. `utils/api_handler.py`

- **Rol:** Comunicación con WhatsApp Business API
- **Funciones:**
  - Simulación de envío de mensajes
  - Formateo de respuestas
  - Manejo de errores de API

---

## 🔒 Seguridad y Buenas Prácticas

- ✅ **Variables de entorno:** Credenciales nunca en código fuente
- ✅ **Validación de entrada:** Sanitización de datos de usuario
- ✅ **Separación de canales:** Comuneros y Especialistas completamente aislados
- ✅ **Logging:** Registro de eventos para auditoría y debugging
- ✅ **Manejo de errores:** Try-catch comprehensivo en puntos críticos

---

## 🐛 Troubleshooting

### El modelo no se encuentra

**Error:** `FileNotFoundError: models/random_forest_model.pkl`

**Solución:** Ejecuta primero el procesador de datos:
```bash
python src/utils/data_processor.py
```

### Errores de importación

**Error:** `ModuleNotFoundError: No module named 'src'`

**Solución:** Asegúrate de ejecutar desde la raíz con:
```bash
python -m src.main_webhook
```

### API de WhatsApp no responde

**Solución:** Verifica que las credenciales en `.env` sean correctas y que tu token no haya expirado.

---

## 📊 Métricas y Monitoreo

El sistema registra las siguientes métricas:

- Número de predicciones realizadas
- Distribución de estados (Verde/Amarillo/Rojo)
- Reportes enviados por comuneros
- Alertas generadas para especialistas
- Tiempo de respuesta del modelo ML

---

## 🚧 Roadmap

### Fase Actual (v1.0)
- ✅ Sistema de predicción ML básico
- ✅ Canales separados Comunero/Especialista
- ✅ Flujos secuenciales de reporte

### Próximas Mejoras (v2.0)
- 🔲 Integración con imágenes satelitales
- 🔲 Dashboard web para especialistas
- 🔲 Notificaciones proactivas basadas en ML
- 🔲 Reentrenamiento automático del modelo
- 🔲 Soporte multiidioma (Quechua/Español)

---

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📞 Contacto y Soporte

Para preguntas, sugerencias o reportar problemas:

- **Issues:** [GitHub Issues](url-del-repositorio/issues)
- **Email:** soporte@ocko-project.org
- **Documentación:** [Wiki del Proyecto](url-del-repositorio/wiki)

---

## 🙏 Agradecimientos

Este proyecto fue desarrollado para apoyar a las comunidades de pastoreo en la gestión sostenible de sus recursos naturales, combinando conocimiento tradicional con tecnología moderna.

**¡Gracias por usar OCKO!** 🌿
