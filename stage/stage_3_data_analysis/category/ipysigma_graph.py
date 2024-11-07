import json
import time
import networkx as nx
from ipysigma import Sigma
import pathlib
from tqdm import tqdm

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

# Input
id_to_category_list_json = category_folder / "step3_id_to_category_remove_uncommon.json"
id_to_similar_id_json = category_folder / "step4_id_to_similar_id.json"

# Output
similarity_graph_html = current_folder / "results" / "similarity_graph.html"

# Load data
with open(id_to_category_list_json, "r", encoding="UTF-8") as file:
    id_to_category_list = json.load(file)
with open(id_to_similar_id_json, "r", encoding="UTF-8") as file:
    id_to_similar_id = json.load(file)

DG = nx.Graph()
for id, id_dict in tqdm(
    id_to_similar_id.items(), total=len(id_to_similar_id), desc="Adding nodes and edges"
):
    DG.add_node(id)

    # Filter similarity value
    id_list = filter(lambda x: x[1] > 2, id_dict.items())

    # Sort id_list by value
    id_list = sorted(id_list, key=lambda x: x[1], reverse=True)[:2]

    for neighbor_id, _ in id_list:
        DG.add_edge(id, neighbor_id)

attrs_dict = {}
for id, categories in id_to_category_list.items():
    attrs_dict[id] = {"categories": categories}
nx.set_node_attributes(DG, attrs_dict)

start_time = time.time()

Sigma(DG, node_color="tag", node_label_size=DG.degree, node_size=DG.degree)

Sigma.write_html(
    DG,
    similarity_graph_html,
    fullscreen=True,
    node_metrics=["louvain"],
    node_color="louvain",
    node_size_range=(3, 20),
    max_categorical_colors=30,
    default_edge_type="rectangle",
    node_border_color_from="node",
    default_node_label_size=14,
    node_size=DG.degree,
)

end_time = time.time()
print(f"{end_time - start_time}s")

# 316.505667924881s
