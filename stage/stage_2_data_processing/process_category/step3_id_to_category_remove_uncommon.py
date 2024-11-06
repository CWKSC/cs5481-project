import json
import pathlib
from tqdm import tqdm

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

# Input
id_to_category_list_json = category_folder / "step1_id_to_category_list.json"
category_to_id_list_json = category_folder / "step2_category_to_id_list.json"

# Output
output_json = category_folder / "step3_id_to_category_remove_uncommon.json"

with open(category_to_id_list_json, "r") as file:
    category_to_id_list = json.load(file)

with open(id_to_category_list_json, "r") as file:
    id_to_category_list = json.load(file)

# Get the number of ids for each category
category_to_num = {}
for category, ids in category_to_id_list.items():
    category_to_num[category] = len(ids)

# Remove uncommon categories (contain less than 3 ids)
result = {}
for id, categories in tqdm(id_to_category_list.items(), total=len(id_to_category_list)):
    result[id] = list(filter(lambda category: category_to_num[category] > 3, categories))

with open(output_json, "w") as file:
    json.dump(result, file, indent=4)
