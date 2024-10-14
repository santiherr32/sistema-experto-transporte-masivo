import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from constants import *

# Cargar el dataset simulado
df = pd.read_csv(DATASET_TRANSPORTE)

# Convertir variables categóricas en numéricas usando LabelEncoder
le = LabelEncoder()
df["Estacion_Origen"] = le.fit_transform(df["Estacion_Origen"])
df["Hora_del_Dia"] = le.fit_transform(df["Hora_del_Dia"])
df["Nivel_de_Trafico"] = le.fit_transform(df["Nivel_de_Trafico"])

# Seleccionar las características relevantes
X = df[["Estacion_Origen", "Hora_del_Dia", "Nivel_de_Trafico", "Cantidad_de_Pasajeros"]]

# Estandarizar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Definir el número de clusters
n_clusters = 4

# Crear e implementar el modelo K-means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X_scaled)

# Obtener los clusters asignados
df["Cluster"] = kmeans.labels_

# Crear una figura grande con subplots (2 filas y 2 columnas)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Subplot 1: Clustering de estaciones de origen y cantidad de pasajeros
axs[0, 0].scatter(X_scaled[:, 0], X_scaled[:, 3], c=df["Cluster"], cmap="viridis", s=50)
axs[0, 0].set_title("Clustering de estaciones de origen y cantidad de pasajeros")
axs[0, 0].set_xlabel("Estación de Origen (Normalizado)")
axs[0, 0].set_ylabel("Cantidad de Pasajeros (Normalizado)")

# Subplot 2: Distribución de Cantidad de Pasajeros por Clúster
sns.boxplot(x="Cluster", y="Cantidad_de_Pasajeros", data=df, ax=axs[0, 1])
axs[0, 1].set_title("Distribución de Cantidad de Pasajeros por Clúster")

# Subplot 3: Distribución de Estaciones de Origen por Clúster
sns.boxplot(x="Cluster", y="Estacion_Origen", data=df, ax=axs[1, 0])
axs[1, 0].set_title("Distribución de Estaciones de Origen por Clúster")

# Subplot 4: Cantidad de Pasajeros vs Nivel de Tráfico por Clúster
sns.scatterplot(
    x="Nivel_de_Trafico",
    y="Cantidad_de_Pasajeros",
    hue="Cluster",
    palette="viridis",
    data=df,
    ax=axs[1, 1],
)
axs[1, 1].set_title("Cantidad de Pasajeros vs Nivel de Tráfico por Clúster")

plt.tight_layout()

# Guardar la figura como una imagen PNG
plt.savefig(IMAGEN_RESULTADOS_NO_SUPERVISADO)
plt.close(fig)  # Cerrar la figura para liberar memoria

# Mostrar mensaje de éxito
print(f"Gráficos guardados exitosamente en '{IMAGEN_RESULTADOS_NO_SUPERVISADO}'")

# Calcular la media por cada clúster (excluyendo columnas de texto)
numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
mean_stats = df.groupby("Cluster")[numeric_columns].mean()

# Mostrar las medias
print("Media de las variables por cada clúster:")
print(mean_stats)

# Calcular la mediana por cada clúster (excluyendo columnas de texto)
median_stats = df.groupby("Cluster")[numeric_columns].median()

# Mostrar las medianas
print("\nMediana de las variables por cada clúster:")
print(median_stats)
