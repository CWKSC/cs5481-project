import json
import time
import networkx as nx
from ipysigma import Sigma
import pathlib

current_folder = pathlib.Path(__file__).parent
datasets_folder = current_folder / 'datasets'
results_folder = current_folder / 'results'

dataset_file = datasets_folder / 'main.json'
output_file = results_folder / 'main.html'

with open(dataset_file, 'r', encoding='UTF-8') as f:
    content = f.read()
    data = json.loads(content)

nodes = data['nodes']
edges = []
for node in nodes:
    for neighbor in nodes:
        if node['id'] != neighbor['id']:
            if set(node['category']) & set(neighbor['category']):
                edges.append((node['id'], neighbor['id']))

DG = nx.DiGraph()
[DG.add_edge(*tuple(edge)) for edge in edges]

attrs_dict = {}
keys_to_extract = ['url']
for node in nodes:
    sub_dict = {key: node[key] for key in keys_to_extract if key in node}
    attrs_dict[node['id']] = sub_dict
nx.set_node_attributes(DG, attrs_dict)

start_time = time.time()

Sigma(
    DG, 
    node_color="tag",
    node_label_size=DG.degree,
    node_size=DG.degree
)

Sigma.write_html(
    DG,
    output_file,
    fullscreen=True,
    node_metrics=['louvain'],
    node_color='louvain',
    node_size_range=(3, 20),
    max_categorical_colors=30,
    default_edge_type='curve',
    node_border_color_from='node',
    default_node_label_size=14,
    node_size=DG.degree
)

end_time = time.time()
print(f'{end_time - start_time}s')
