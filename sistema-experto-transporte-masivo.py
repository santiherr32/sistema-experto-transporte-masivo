import networkx as nx

# Crear el grafo de estaciones y rutas
G = nx.Graph()

# Agregar nodos (Estaciones)
G.add_nodes_from(["Estación A", "Estación B", "Estación C", "Estación D"])

# Agregar aristas (Rutas) con pesos (Distancias en minutos)
G.add_edge("Estación A", "Estación B", weight=5)
G.add_edge("Estación A", "Estación C", weight=10)
G.add_edge("Estación B", "Estación C", weight=2)
G.add_edge("Estación B", "Estación D", weight=7)
G.add_edge("Estación C", "Estación D", weight=3)

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


estacion_origen = "Estación B"
estacion_destino = "Estación C"

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
