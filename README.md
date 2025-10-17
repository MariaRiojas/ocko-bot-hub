# 🌿 OCKO: Bot de WhatsApp para Monitoreo y Gestión de Pastizales

Ocko es un proyecto de chatbot diseñado para ofrecer servicios de monitoreo y gestión de pastizales a través de WhatsApp. Se dirige a dos audiencias clave: **Comuneros** (alertas y consejos rápidos) y **Especialistas** (validación de modelos y gestión de datos).

El sistema utiliza **Machine Learning (ML) avanzado** (Random Forest Classifier) para predecir el estado de salud del pastizal (Semáforo: Verde, Amarillo, Rojo) basándose en indicadores de campo como el vigor de las plantas y el grado de utilización.

---

## 🚀 1. Estructura y Componentes del Proyecto

El proyecto sigue una arquitectura modular y escalable en Python.

/ocko_whatsapp_project ├── /data │ ├── /raw # Datos originales (CSVs de campo) │ └── /processed # Indicadores consolidados (ML_Grassland_Indicators.csv) ├── /models │ ├── random_forest_model.pkl # Modelo ML entrenado (para predicciones rápidas) │ └── label_encoder.pkl # Codificador de clases ('Green', 'Yellow', 'Red') ├── /src # Código fuente de la aplicación │ ├── data_processor.py # Limpieza, ML, entrenamiento y guardado de modelos │ └── whatsapp_bot.py # Lógica del bot, flujos y simulación de la API ├── .env # Variables de entorno y credenciales └── requirements.txt # Dependencias de Python (pandas, scikit-learn, joblib, etc.)

---

## 🛠️ 2. Configuración del Ambiente de Desarrollo

### 2.1. Instalación y Entorno Virtual

1.  **Instalar Dependencias:** Crea y activa tu entorno virtual (`venv`).
2.  **Instalar Librerías:** Instala las dependencias listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### 2.2. Preparación de Datos y Credenciales

1.  **Datos:** Coloca los archivos CSV de tus datos de campo en la carpeta **`data/raw`**. Asegúrate de que los archivos clave para el ML usen los nombres simplificados:
    * `Data_DispoGrass.csv`
    * `Data_PlantVigor.csv`
    * `Data_SpeciesUtilization.csv`

2.  **Credenciales (`.env`):** Edita el archivo **`.env`** en la raíz del proyecto para incluir tus credenciales de la API de WhatsApp Business Cloud (Meta):

    ```bash
    # .env
    WHATSAPP_API_TOKEN="TU_TOKEN_DE_ACCESO_DE_META"
    WHATSAPP_API_URL="URL_DEL_ENDPOINT_DE_META/messages"
    # El bot usará estas variables en la función 'send_whatsapp_message' simulada.
    ```

---

## ⚙️ 3. Flujo de Procesamiento de Datos (ML)

El script **`data_processor.py`** es la columna vertebral del sistema de inteligencia, ya que consolida la data y entrena el modelo de predicción.

### 3.1. Ejecución del Procesador

Ejecuta el script desde la raíz del proyecto para generar el modelo y los indicadores:

```bash
python src/data_processor.py