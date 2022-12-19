import networkx as nx
import matplotlib.pyplot as plt

def bellman_ford(graph, source):
    # Шаг 1: Подготовление расстояния и предшественника для каждого узла
    distance, predecessor = dict(), dict()
    full_path = []
    for node in graph:
        distance[node], predecessor[node] = float('inf'), None
    distance[source] = 0

    # Шаг 2: Релаксирование вершин
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbour in graph[node]:
                # Если расстояние между узлом и соседом меньше текущего - сохраняем
                if distance[neighbour] > distance[node] + graph[node][neighbour]:
                    # graph[node][neighbour]] - вес между node и neighbour
                    full_path.append([node, neighbour])
                    distance[neighbour], predecessor[neighbour] = distance[node] + graph[node][neighbour], node

    # Шаг 3: Проверка наличия отрицательных циклов
    for node in graph:
        for neighbour in graph[node]:
            assert distance[neighbour] <= distance[node] + graph[node][neighbour], "Негативный взвешенный цикл"
 
    return distance, predecessor, full_path

def draw_graf():
    colors = nx.get_edge_attributes(G,'color').values()  
    nx.draw(G, pos, edge_color=colors, with_labels=True, font_weight='bold',)
    edge_weight = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
    plt.show()

def change_edge_colors(color):
    # Красим ребра графа в произвольный цвет
    for e1, e2 in G.edges(): G[e1][e2]['color'] = color

def display_graf(edges):
    change_edge_colors('black')
    # Красим ребро между r1 и r2 в красный цвет
    for r1, r2 in edges:
        for e1, e2 in G.edges():
            if r1 == e1 and r2 == e2 or r1 == e2 and r2 == e1:
                G[e1][e2]['color'] = 'red'
                # Отображаем граф, если edges - список
                if type(edges) is list: draw_graf()
    # Отображаем граф, если edges - словарь
    if type(edges) is not list: draw_graf()
    change_edge_colors('black')

def dict_to_graph(graph):
    edges = []
    for node in graph:
        #print(node, graph[node])
        for neighbour in graph[node]:
            edges.append((node, neighbour, graph[node][neighbour]))
            #print((node, neighbour, graph[node][neighbour]))
    return edges

graph = {
    'z': {'u': 6, 'x': 7},
    'u': {'y': -4, 'x': 8},
    'v': {'u': -2},
    'x': {'v': -3, 'y': 9},
    'y': {'z': 2, 'v': 7}}

print('Dict', graph)
dist, path, fpath = bellman_ford(graph, source='z')
print('Текущий вес:', dist)
print('Путь:', path)
print('Полный путь:', fpath)

edges = dict_to_graph(graph)
print('DiGraph', edges)
G = nx.DiGraph(edges)
#G.add_weighted_edges_from(edges)
pos = nx.circular_layout(G)

display_graf(fpath)
print('Покрасили черным. Показываем конечный результат')
draw_graf()
display_graf(path.items())