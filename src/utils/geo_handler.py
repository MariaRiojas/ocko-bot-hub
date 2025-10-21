# src/utils/geo_handler.py

import numpy as np

def read_tif_ndvi(zone_id):
    """
    Simula la lectura de un archivo .tif para obtener un valor de NDVI y una imagen.
    En la vida real, usaría librerías como GDAL o rasterio.
    """
    print(f"   [GEO]: Accediendo a archivos .tif en /data/raw/geospatial para {zone_id}...")
    
    # Simulación de un valor NDVI promedio y una imagen
    ndvi_value = np.random.uniform(0.4, 0.7) # Valores típicos de pastizales
    image_ref = f"img_ndvi_{zone_id}.png"
    
    return ndvi_value, image_ref

def process_image_for_cnn(local_path):
    """
    Simula la preparación de una imagen (enviada por el comunero) para el modelo CNN.
    """
    # En la vida real: resize, normalización, conversión a tensor.
    print(f"   [GEO]: Preprocesando imagen {local_path} para clasificación CNN...")
    return np.zeros((1, 224, 224, 3)) # Tensor simulado