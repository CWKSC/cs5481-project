import json
import pathlib
from tqdm import tqdm
import matplotlib.pyplot as plt  # New import for plotting

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"
json_folder = resources_folder / "json"

input_json = json_folder / "category_to_id_list.json"  # Input from step 2

with open(input_json, "r") as file:
    data = json.load(file)

# Filter out categories with only one ID
filtered_data = {category: ids for category, ids in data.items() if len(ids) > 1}

# Save the filtered data to a new JSON file
output_json = json_folder / "category_to_id_list_filtered.json"
with open(output_json, "w") as file:
    json.dump(filtered_data, file, indent=4)


