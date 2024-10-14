import os
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow import keras
from constants import *

# Cargar el dataset
df = pd.read_csv(DATASET_TRANSPORTE)
print(f"El dataset contiene {len(df)} registros")

# Convertir variables categóricas en numéricas usando LabelEncoder
le = LabelEncoder()
df["Estacion_Origen"] = le.fit_transform(df["Estacion_Origen"])
df["Hora_del_Dia"] = le.fit_transform(df["Hora_del_Dia"])
df["Dia_de_la_Semana"] = le.fit_transform(df["Dia_de_la_Semana"])
df["Nivel_de_Trafico"] = le.fit_transform(df["Nivel_de_Trafico"])
df["Clima"] = le.fit_transform(df["Clima"])

# Generar características adicionales
df["Trafico_Hora"] = df["Nivel_de_Trafico"] * df["Hora_del_Dia"]
df["Congestion_Hora"] = df["Indice_de_Congestion"] * df["Hora_del_Dia"]

# Eliminar variables con correlación baja
df = df.drop(
    columns=[
        "Estacion_Origen",
        "Hora_del_Dia",
        "Clima",
        "Trafico_Hora",
        "Dia_de_la_Semana",
    ]
)

# Calcular la matriz de correlación
correlation_matrix = df.corr()
# Mostrar la correlación con la variable objetivo 'Cantidad_de_Pasajeros' de las variables incluidas
print("Matriz de correlación con la variable 'Cantidad_de_Pasajeros': ")
print(correlation_matrix["Cantidad_de_Pasajeros"])

# Separar características y variable objetivo
X = df.drop(columns=["Cantidad_de_Pasajeros"])
y = df["Cantidad_de_Pasajeros"]

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Escalar características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Definir la red neuronal profunda
model = keras.Sequential(
    [
        keras.Input(shape=(X_train_scaled.shape[1],)),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1),  # Salida para la regresión
    ]
)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse", metrics=["mae"]
)

# Entrenar el modelo
history = model.fit(
    X_train_scaled,
    y_train,
    validation_data=(X_test_scaled, y_test),
    validation_split=0.2,
    epochs=100,
    batch_size=64,
    verbose=1,
)

# Obtener los MAE de entrenamiento y validación
mae_train = history.history["mae"][-1]  # Última época - MAE en entrenamiento
mae_val = history.history["val_mae"][-1]  # Última época - MAE en validación

# Evaluar en el conjunto de prueba
test_loss, test_mae = model.evaluate(X_test_scaled, y_test)
print(f"MAE en el conjunto de prueba: {test_mae}")

from fpdf import FPDF
from datetime import datetime
import os
from PyPDF2 import PdfReader, PdfWriter

# Archivos de resultados y conteo

# Verificar si los archivos PDF y de conteo existen y si no, iniciar desde cero
if not os.path.exists(PDF_FILENAME) and not os.path.exists(COUNT_FILENAME):
    num_pruebas = 0  # Si no existen, comenzar desde la primera prueba
else:
    # Verificar si el archivo de conteo existe y leer el número de pruebas
    if os.path.exists(COUNT_FILENAME):
        with open(COUNT_FILENAME, "r") as f:
            num_pruebas = int(f.read().strip())
    else:
        num_pruebas = 0

# Incrementar el número de pruebas
num_pruebas += 1

# Guardar el nuevo número de pruebas en el archivo de conteo
with open(COUNT_FILENAME, "w") as f:
    f.write(str(num_pruebas))

# Crear un nuevo PDF para la prueba actual
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Agregar una nueva prueba con su numeración
pdf.set_font("Arial", size=10, style="B")
pdf.cell(200, 10, txt=f"Prueba #{num_pruebas}", ln=True)
pdf.set_font("Arial", size=10)
pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
pdf.cell(200, 10, txt=f"Max Pasajeros: {MAX_PASSENGERS_AMOUNT}", ln=True)
pdf.cell(200, 10, txt=f"Registros: {len(df)}", ln=True)
pdf.cell(200, 10, txt=f"MAE Entrenamiento: {mae_train}", ln=True)
pdf.cell(200, 10, txt=f"MAE Validación: {mae_val}", ln=True)
pdf.cell(200, 10, txt=f"MAE Prueba: {test_mae}", ln=True)

# Guardar el PDF de la prueba actual en un archivo temporal
new_PDF_FILENAME = "nuevo_bloque_prueba.pdf"
pdf.output(new_PDF_FILENAME)

# Si el PDF principal ya existe, combinarlo con el nuevo bloque
if os.path.exists(PDF_FILENAME):
    reader = PdfReader(PDF_FILENAME)
    writer = PdfWriter()

    # Copiar todas las páginas del PDF existente
    for page_num in range(len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    # Añadir la nueva página con la prueba actual
    new_pdf = PdfReader(new_PDF_FILENAME)
    writer.add_page(new_pdf.pages[0])

    # Guardar el archivo combinado
    with open(PDF_FILENAME, "wb") as output_pdf:
        writer.write(output_pdf)

    # Eliminar el archivo temporal
    os.remove(new_PDF_FILENAME)

else:
    # Si no existe el PDF, renombrar el nuevo PDF como el archivo principal
    os.rename(new_PDF_FILENAME, PDF_FILENAME)

print(f"Resultados guardados en '{PDF_FILENAME}'")
