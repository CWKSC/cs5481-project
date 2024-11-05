# Tutorial:
# https://medium.com/@msdatashift/ipysigma-easily-visualize-networks-with-thousands-of-nodes-and-edges-in-python-3ecdbe0321de

# Dataset get from https://github.com/jacomyal/sigma.js/blob/main/packages/demo/public/dataset.json

import json
import time
import networkx as nx
from ipysigma import Sigma

import pathlib

current_folder = pathlib.Path(__file__).parent
datasets_folder = current_folder / 'datasets'
results_folder = current_folder / 'results'

dataset_file = datasets_folder / 'tutorial.json'
output_file = results_folder / 'tutorial.html'

with open(dataset_file, 'r', encoding='UTF-8') as f:
    content = f.read()
    data = json.loads(content)

DG = nx.DiGraph()

[DG.add_edge(*tuple(edge)) for edge in data['edges']]

attrs_dict = {}
keys_to_extract = ['label','tag','URL']
for node_attrs in data['nodes']:
    node = node_attrs['key']
    sub_dict = {key: node_attrs[key] for key in keys_to_extract if key in node_attrs}
    attrs_dict[node] = sub_dict
nx.set_node_attributes(DG, attrs_dict)

# Need around 19.5s
start_time = time.time()
nx.draw(DG, with_labels=True)
end_time = time.time()
print(f'{end_time - start_time}s')

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

