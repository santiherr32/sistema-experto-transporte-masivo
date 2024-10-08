import networkx as nx

# Crear el grafo de estaciones y rutas
G = nx.Graph()

# Agregar nodos (Estaciones en un sector de Bogotá)
G.add_nodes_from([
    "Portal de la 80", "Avenida Cali", "Carrera 68",
    "Estadio El Campín", "Universidad Nacional",
    "Centro Internacional", "Las Aguas"
])

# Agregar aristas (Rutas) con pesos (Distancias en minutos)
G.add_edge("Portal de la 80", "Avenida Cali", weight=10)
G.add_edge("Avenida Cali", "Carrera 68", weight=8)
G.add_edge("Carrera 68", "Estadio El Campín", weight=7)
G.add_edge("Estadio El Campín", "Universidad Nacional", weight=5)
G.add_edge("Universidad Nacional", "Centro Internacional", weight=6)
G.add_edge("Centro Internacional", "Las Aguas", weight=4)
G.add_edge("Portal de la 80", "Universidad Nacional", weight=20)
G.add_edge("Carrera 68", "Centro Internacional", weight=12)

# Definir base de conocimiento (reglas)


def aplicar_reglas_logicas(G, origen, destino):
    """
    Esta función crea un subgrafo basado en las reglas lógicas que guían la selección de rutas en el sistema de transporte.
    """
    # Crear un subgrafo vacío
    subgrafo = nx.Graph()

    # Regla 1: Si existe una ruta directa entre origen y destino, consíderala
    if G.has_edge(origen, destino):
        subgrafo.add_edge(origen, destino, weight=G[origen][destino]['weight'])

    # Regla 2: Si hay una ruta indirecta (en un solo paso) que conecta origen y destino, consíderala
    for node in G.neighbors(origen):
        if G.has_edge(node, destino):
            # Agregar ambos tramos (origen -> node) y (node -> destino) al subgrafo
            subgrafo.add_edge(origen, node, weight=G[origen][node]['weight'])
            subgrafo.add_edge(node, destino, weight=G[node][destino]['weight'])

    # Retornar el subgrafo con las rutas seleccionadas por las reglas
    return subgrafo


# Estaciones de prueba para el sector de Bogotá
estacion_origen = "Portal de la 80"
estacion_destino = "Las Aguas"

# Crear un subgrafo basado en las reglas lógicas
subgrafo_filtrado = aplicar_reglas_logicas(
    G, estacion_origen, estacion_destino)

# Verificamos si el subgrafo tiene rutas válidas
if len(subgrafo_filtrado.edges) > 0:
    # Usar Dijkstra sobre el subgrafo filtrado
    try:
        ruta_mas_corta = nx.dijkstra_path(
            subgrafo_filtrado, source=estacion_origen, target=estacion_destino)
        distancia_mas_corta = nx.dijkstra_path_length(
            subgrafo_filtrado, source=estacion_origen, target=estacion_destino)
        print(f"La ruta más corta desde la {estacion_origen} hasta la {
              estacion_destino} en el subgrafo es: {ruta_mas_corta}")
        print(f"Con una distancia total de: {distancia_mas_corta} minutos")
    except nx.NetworkXNoPath:
        print(f"No hay una ruta posible entre la {estacion_origen} y la {
              estacion_destino} bajo las reglas definidas.")
else:
    print("No hay rutas válidas basadas en las reglas lógicas.")
