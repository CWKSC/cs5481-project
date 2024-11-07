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
category_to_id_list_json = category_folder / "step2_category_to_id_list.json"
id_to_category_list_json = category_folder / "step3_id_to_category_top_30.json"
id_to_similar_id_from_top_30_json = (
    category_folder / "step4_id_to_similar_id_from_top_30.json"
)

# Output
progressive_html = current_folder / "results" / "progressive.html"

# Load data
with open(category_to_id_list_json, "r", encoding="UTF-8") as file:
    category_to_id_list = json.load(file)
with open(id_to_category_list_json, "r", encoding="UTF-8") as file:
    id_to_category_list = json.load(file)
with open(id_to_similar_id_from_top_30_json, "r", encoding="UTF-8") as file:
    id_to_similar_id = json.load(file)

# Get id to category length
id_to_category_length = {
    id: len(categories) for id, categories in id_to_category_list.items()
}

DG = nx.Graph()

# Get id to category list length
id_to_category_list_length = {
    id: len(categories) for id, categories in id_to_category_list.items()
}

# Get top 30 categories
top_categories = sorted(
    category_to_id_list.items(), key=lambda x: len(x[1]), reverse=True
)[2 : 2 + 30]
for category, id_list in tqdm(top_categories, desc="Link categories"):
    DG.add_node(f"tag-{category}")

    # Filter the only category in id_to_category_list
    id_list = filter(lambda id: id_to_category_list_length[id] <= 2, id_list)

    # Sort id_list by id_to_category_list_length
    id_list = sorted(id_list, key=lambda id: id_to_category_list_length[id])

    for id in id_list[:40]:
        DG.add_edge(f"tag-{category}", id)

def sort_by_similarity_key_function(element):
    if len(element[1]) == 0:
        return 0
    return max(element[1].values())


def sort_by_similarity():
    global id_to_similar_id
    id_to_similar_id = dict(
        sorted(
            id_to_similar_id.items(), key=sort_by_similarity_key_function, reverse=True
        )
    )
    # first_element = list(id_to_similar_id.keys())[0]
    # print(id_to_similar_id[first_element])

pbar = tqdm(total=len(id_to_similar_id.keys()), desc="Progressive")
counting_table = {}
while len(id_to_similar_id.keys()) > 0:
    sort_by_similarity()
    first_key = next(iter(id_to_similar_id))
    first_value_ids = id_to_similar_id[first_key]

    if len(first_value_ids) == 0:
        del id_to_similar_id[first_key]
        pbar.update(1)
        continue
    first_value = list(first_value_ids.keys())[0]

    # Connect
    DG.add_edge(first_key, first_value)
    counting_table[first_value] = counting_table.get(first_value, 0) + 1
    counting_table[first_key] = counting_table.get(first_key, 0) + 1

    # Remove
    if first_key in id_to_similar_id:
        if first_value in id_to_similar_id[first_key]:
            del id_to_similar_id[first_key][first_value]
    if first_value in id_to_similar_id:
        if first_key in id_to_similar_id[first_value]:
            del id_to_similar_id[first_value][first_key]

    # Remove if counting to max connection
    # max_connection = 4
    if counting_table[first_key] >= max(3, id_to_category_length[first_key]):
        if first_key in id_to_similar_id:
            del id_to_similar_id[first_key]
            pbar.update(1)
        for id, id_dict in id_to_similar_id.items():
            if first_key in id_dict:
                del id_dict[first_key]
    if counting_table[first_value] >= max(3, id_to_category_length[first_value]):
        if first_value in id_to_similar_id:
            del id_to_similar_id[first_value]
            pbar.update(1)
        for id, id_dict in id_to_similar_id.items():
            if first_value in id_dict:
                del id_dict[first_value]

    # if len(id_to_similar_id.keys()) % 5 == 0:
    #     print(
    #         len(id_to_similar_id.keys()),
    #         first_key,
    #         first_value,
    #         counting_table[first_key],
    #         counting_table[first_value],
    #     )

pbar.close()


attrs_dict = {}
for id, categories in id_to_category_list.items():
    attrs_dict[id] = {"categories": categories}
nx.set_node_attributes(DG, attrs_dict)

start_time = time.time()

Sigma(DG, node_color="tag", node_label_size=DG.degree, node_size=DG.degree)

Sigma.write_html(
    DG,
    progressive_html,
    default_edge_type="curve",
    default_node_label_size=16,
    fullscreen=True,
    # label_rendered_size_threshold=30,
    max_categorical_colors=30,
    node_border_color_from="node",
    node_color="louvain",
    node_metrics=["louvain"],
    node_size_range=(3, 20),
    node_size=DG.degree,
)

end_time = time.time()
print(f"{end_time - start_time}s")

# 316.505667924881s
