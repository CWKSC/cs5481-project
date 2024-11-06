from tqdm import tqdm
import json
import pathlib

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

input_json = category_folder / "step1_id_to_category_list.json"
output_json = category_folder / "step2_category_to_id_list.json"

with open(input_json, "r") as file:
    data = json.load(file)

result = {}
for key, values in tqdm(data.items(), total=len(data)):
    for value in values:
        # Initialize the list for the category if it doesn't exist
        if value not in result:
            result[value] = []
        # Append the ID to the category list
        result[value].append(key)

with open(output_json, "w") as file:
    json.dump(result, file, indent=4)
