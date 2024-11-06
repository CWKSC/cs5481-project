import json
import pathlib
from tqdm import tqdm

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

# Input
id_to_category_list_json = category_folder / "step3_id_to_category_remove_uncommon.json"

# Output
output_json = category_folder / "step4_id_to_similar_id.json"

with open(id_to_category_list_json, "r") as file:
    id_to_category_list = json.load(file)

result = {}
for id, categories in tqdm(id_to_category_list.items(), total=len(id_to_category_list), desc="Get similarity of each id"):
    similarity = {}
    for other_id, other_categories in id_to_category_list.items():
        if id == other_id:
            continue

        # Get the number of categories that are the same between two ids
        similarity_value = len(set(categories) & set(other_categories))
        if similarity_value == 0:
            continue
        similarity[other_id] = similarity_value
    
    # Keep only top 10 similar ids
    similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True)[:10])
    result[id] = similarity

with open(output_json, "w") as file:
    json.dump(result, file, indent=4)
