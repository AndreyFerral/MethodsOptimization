import networkx as nx
import matplotlib.pyplot as plt

def bellman_ford(graph, source):
    # Step 1: Prepare the distance and predecessor for each node
    distance, predecessor = dict(), dict()
    full_path = []
    for node in graph:
        distance[node], predecessor[node] = float('inf'), None
    distance[source] = 0

    # Step 2: Relax the edges
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbour in graph[node]:
                # If the distance between the node and the neighbour is lower than the current, store it
                if distance[neighbour] > distance[node] + graph[node][neighbour]:
                    full_path.append([node, neighbour, graph[node][neighbour]])
                    distance[neighbour], predecessor[neighbour] = distance[node] + graph[node][neighbour], node

    # Step 3: Check for negative weight cycles
    for node in graph:
        for neighbour in graph[node]:
            assert distance[neighbour] <= distance[node] + graph[node][neighbour], "Negative weight cycle."
 
    return distance, predecessor, full_path

def draw_graf():
    colors = nx.get_edge_attributes(G,'color').values()  
    nx.draw(G, pos, edge_color=colors, with_labels=True, font_weight='bold',)
    edge_weight = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
    plt.show()

def dict_to_graph(graph):
    edges = []
    for node in graph:
        #print(node, graph[node])
        for neighbour in graph[node]:
            edge = (node, neighbour, graph[node][neighbour])
            edges.append(edge)
            #print(edge)
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
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

for e1, e2 in G.edges(): G[e1][e2]['color'] = 'black'
pos = nx.circular_layout(G)

for r1, r2, w in fpath:
    for e1, e2 in G.edges():
        if r1 == e1 and r2 == e2 or r1 == e2 and r2 == e1:
            G[e1][e2]['color'] = 'red'
            draw_graf()

for e1, e2 in G.edges(): 
    G[e1][e2]['color'] = 'black'

print('Покрасили черным. Отображаем путь')
draw_graf()

for r1, r2 in path.items():
    for e1, e2 in G.edges():
        if r1 == e1 and r2 == e2 or r1 == e2 and r2 == e1:
            G[e1][e2]['color'] = 'red'

draw_graf()