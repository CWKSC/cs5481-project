from tqdm import tqdm
import json
import pathlib

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

# Input
id_to_category_list_json = category_folder / "step1_id_to_category_list.json"
category_to_id_list_json = category_folder / "step2_category_to_id_list.json"

# Output
id_to_category_remove_uncommon_json = (
    category_folder / "step3_id_to_category_remove_uncommon.json"
)
id_to_category_top_30_json = category_folder / "step3_id_to_category_top_30.json"

# Load data
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
for id, categories in tqdm(
    id_to_category_list.items(),
    total=len(id_to_category_list),
    desc="Remove uncommon categories",
):
    result[id] = list(
        filter(lambda category: category_to_num[category] > 3, categories)
    )

# Save result
with open(id_to_category_remove_uncommon_json, "w") as file:
    json.dump(result, file, indent=4)

# Get top n categories
top_n = 30
top_n_categories = dict(
    sorted(category_to_num.items(), key=lambda item: item[1], reverse=True)[
        2 : 2 + top_n
    ]
)

result = {}
for id, categories in tqdm(
    id_to_category_list.items(),
    total=len(id_to_category_list),
    desc=f"Remove categories not in top {top_n}",
):
    result_list = list(
        filter(lambda category: category in top_n_categories, categories)
    )
    if len(result_list) > 0:
        result[id] = result_list

# Save result
with open(id_to_category_top_30_json, "w") as file:
    json.dump(result, file, indent=4)
