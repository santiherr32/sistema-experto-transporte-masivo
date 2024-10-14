# Sistema de Transporte Masivo - Modelos Supervisado y No Supervisado

Este repositorio contiene dos implementaciones de sistemas de análisis para el transporte masivo simulado, en el contexto de actividades de modelado predictivo y análisis de patrones en los datos. El sistema de transporte evoca el Transmilenio de Bogotá, usando datos simulados para predecir la cantidad de pasajeros en diferentes situaciones.

## Contenido del Repositorio

- **generador_dataset_local.py**: Genera datasets simulados para el sistema de transporte. Contiene variables como estaciones, hora del día, nivel de tráfico, y cantidad de pasajeros. Este script permite variar el tamaño del dataset y el número máximo de pasajeros.

- **modelo_supervisado_redes_neuronales.py**: Implementa un sistema supervisado basado en redes neuronales para predecir la cantidad de pasajeros en las estaciones, considerando variables como el nivel de tráfico, hora del día, y clima. Incluye el uso de Dropout y técnicas de regularización para mejorar el rendimiento del modelo.

- **modelo_no_supervisado_clustering.py**: Implementa un sistema no supervisado de clustering usando KMeans para agrupar los datos según características como estación de origen, nivel de tráfico, y cantidad de pasajeros. Además, genera gráficos que ayudan a visualizar los resultados y agrupa las variables en diferentes clústeres.

## Sistema Supervisado:

En esta actividad, se implementó un modelo de **Redes Neuronales** para predecir la cantidad de pasajeros en diferentes estaciones de un sistema de transporte masivo simulado. Se utilizaron técnicas de preprocesamiento de datos, ingeniería de características, y regularización (como Dropout) para mejorar el rendimiento del modelo. 

### Modelo:
- **Redes Neuronales**: Predecir la cantidad de pasajeros usando variables como la estación de origen, hora del día, nivel de tráfico, entre otras.
- **Resultados**: El modelo logra un MAE promedio de alrededor de 93 pasajeros (en un rango máximo de 2000 pasajeros), considerado aceptable para los fines del sistema.
  
### Archivos:
- `modelo_supervisado_redes_neuronales.py`: Script principal que entrena y evalúa el modelo supervisado.
- **PDF de Resultados**: Los resultados de cada prueba del modelo se almacenan en un archivo PDF.

## Sistema No Supervisado:

En esta actividad, se implementó un modelo de **clustering KMeans** para analizar y segmentar los datos del sistema de transporte. El objetivo fue identificar patrones de comportamiento entre las estaciones y los pasajeros. Se utilizó **KMeans** para agrupar los datos y se generaron varios gráficos que muestran las distribuciones y características de los clústeres.

### Modelo:
- **KMeans Clustering**: Agrupamiento de estaciones y pasajeros según variables como la cantidad de pasajeros, nivel de tráfico, y hora del día.
- **Resultados**: Se visualizaron 4 clústeres y se generaron gráficos para representar visualmente las distribuciones.

### Archivos:
- `modelo_no_supervisado_clustering.py`: Script principal que agrupa los datos y genera los gráficos correspondientes.
- **CSV de Resultados**: El dataset con los clústeres asignados a cada fila se guarda en un archivo CSV.
- **Gráficos PNG**: Se genera una imagen con múltiples gráficos que visualizan los resultados del clustering.

## Requisitos

- Python 3.8+
- Librerías: 
  - `scikit-learn`
  - `matplotlib`
  - `seaborn`
  - `fpdf` (para el sistema supervisado)
  - `pandas`
  - `numpy`

## Uso

### 1. Generar el Dataset
Ejecuta el script `generador_dataset_local.py` para generar un dataset simulado con el número de pasajeros, nivel de tráfico, y otras características relevantes.
Puedes definir la cantidad maxima de pasajeros y el número de registros del dataset cambiando las constantes correspondientes en el archivo `constants.py`

```bash
python generador_dataset_local.py
```

### 2. Entrenar y Evaluar el Modelo Supervisado

```bash
python modelo_supervisado_redes_neuronales.py
```

### 3. Ejecutar el Clustering No Supervisado

```bash
python modelo_no_supervisado_clustering.py
```
