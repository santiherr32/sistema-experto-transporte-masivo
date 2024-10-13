import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Cargar el dataset simulado
df = pd.read_csv("dataset_transporte_simulado.csv")

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

# Definir el número de clusters (puedes ajustar este valor según lo necesites)
n_clusters = 4

# Crear e implementar el modelo K-means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X_scaled)

# Obtener los clusters asignados
df["Cluster"] = kmeans.labels_

# Visualización simple de los clusters
plt.figure(figsize=(8, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 3], c=df["Cluster"], cmap="viridis", s=50)
plt.title("Clustering de estaciones de origen y cantidad de pasajeros")
plt.xlabel("Estación de Origen (Normalizado)")
plt.ylabel("Cantidad de Pasajeros (Normalizado)")
plt.colorbar(label="Cluster")
plt.show()

# Guardar los resultados en un CSV
df.to_csv("dataset_transporte_clustering.csv", index=False)
print("Dataset con clusters guardado en 'dataset_transporte_clustering.csv'")
