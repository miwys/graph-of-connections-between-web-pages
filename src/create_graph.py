import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

G = nx.Graph(day="external_links_scraping")
df_nodes = pd.read_csv('nodes.csv', error_bad_lines=False)
df_edges = pd.read_csv('edges.csv', error_bad_lines=False)

for index, row in df_nodes.iterrows():
    G.add_node(row['name'])
    
for index, row in df_edges.iterrows():
    G.add_weighted_edges_from([(row['source'], row['target'], row['value'])])
    
plt.figure(figsize=(20,20))
options = {
    'edge_color': '#23cc4d',
    'width': 1,
    'with_labels': True,
    'font_weight': 'regular',
}
nx.draw(G, node_color='#3723cc', node_size=200, pos=nx.spring_layout(G, k=0.25, iterations=150), **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#ff0505") 
plt.savefig('graph.png')
plt.show()
