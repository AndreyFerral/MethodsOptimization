import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from random import random, randint

def draw_graf():
    colors = nx.get_edge_attributes(G,'color').values()  
    nx.draw(G, pos, edge_color=colors, with_labels=True, font_weight='bold',)
    edge_weight = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
    plt.show()

def ER(n, p):
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        a = random()
        if a < p:
            a, b = combination
            if a > b: a, b = b, a 
            E.add((a, b, randint(-10, 10)))
    return list(E)

G = nx.DiGraph(directed=True) 
n, p = 7, 0.5
E = ER(n, p)
print('Граф', E)

G.add_weighted_edges_from(E)
for e1, e2 in G.edges(): G[e1][e2]['color'] = 'black'
pos = nx.circular_layout(G)

try:
    source, target = 0, 3
    length, path = nx.single_source_bellman_ford(G, source, target)
    print('Путь', path)
    print('Длина', length)

    for r1, r2 in zip(path, path[1:]):
        for e1, e2 in G.edges():
            if r1 == e1 and r2 == e2 or r1 == e2 and r2 == e1:
                if path[-1] == r2:
                    print('Это последняя демонстрация метода белмана-форда')
                G[e1][e2]['color'] = 'red'
                draw_graf()
except:
    print(f'Ошибка! Отсутствие пути, источника или цели ({source}, {target})')
    draw_graf()