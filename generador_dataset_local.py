import pandas as pd
import numpy as np
from constants import *

# Definir las estaciones disponibles
estaciones = [
    "Portal de la 80",
    "Avenida Cali",
    "Carrera 68",
    "Estadio El Campín",
    "Universidad Nacional",
    "Centro Internacional",
    "Las Aguas",
]

# Crear un array de estaciones de origen aleatorio
estacion_origen = np.random.choice(estaciones, DATA_LENGTH)

# Crear un array de estaciones de destino aleatorio que sea diferente al origen
estacion_destino = [
    np.random.choice([dest for dest in estaciones if dest != origen])
    for origen in estacion_origen
]

# Simular un dataset mejorado
data = {
    "Estacion_Origen": estacion_origen,
    # "Estacion_Destino": estacion_destino,
    "Hora_del_Dia": np.random.choice(
        ["6:00 AM", "7:00 AM", "8:00 AM", "5:00 PM", "6:00 PM", "7:00 PM"], DATA_LENGTH
    ),
    "Dia_de_la_Semana": np.random.choice(
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], DATA_LENGTH
    ),
    "Nivel_de_Trafico": np.random.choice(
        ["Bajo", "Medio", "Alto"], DATA_LENGTH, p=[0.3, 0.5, 0.2]
    ),
    "Tiempo_de_Viaje_min": np.random.randint(15, 50, DATA_LENGTH),
    "Indice_de_Congestion": np.random.rand(DATA_LENGTH),
    "Clima": np.random.choice(
        ["Soleado", "Lluvioso", "Nublado"], DATA_LENGTH, p=[0.6, 0.3, 0.1]
    ),
    # "Hora_del_Dia_Minutos": np.random.choice(
    #     [360, 420, 480, 1020, 1080, 1140], DATA_LENGTH
    # ),
}

# Generar Cantidad_de_Pasajeros en función de otras variables
np.random.seed(42)
nivel_trafico_map = {"Bajo": 0.5, "Medio": 1.0, "Alto": 1.5}

# Calcular los pasajeros con un valor base y escalar según MAX_PASSENGERS_AMOUNT
raw_passenger_count = (
    50  # Constante base
    + 5
    * data[
        "Tiempo_de_Viaje_min"
    ]  # Aumentar el peso de la variable 'Tiempo_de_Viaje_min'
    + 50
    * data[
        "Indice_de_Congestion"
    ]  # Ajustar el peso de la variable 'Indice_de_Congestion'
    + np.vectorize(nivel_trafico_map.get)(data["Nivel_de_Trafico"])
    * 100  # Impacto del nivel de tráfico
    + np.random.randint(-50, 50, DATA_LENGTH)  # Introducir variabilidad
)

# Escalar los valores generados para que respeten el límite de MAX_PASSENGERS_AMOUNT
data["Cantidad_de_Pasajeros"] = (
    raw_passenger_count / raw_passenger_count.max() * MAX_PASSENGERS_AMOUNT
).clip(0, MAX_PASSENGERS_AMOUNT)

# Creando el DataFrame
df = pd.DataFrame(data)

# Guardar el nuevo dataset simulado en un archivo CSV
df.to_csv("dataset_transporte_simulado.csv", index=False)
print(f"Archivo dataset_transporte_simulado.csv guardado con {DATA_LENGTH} registros")
