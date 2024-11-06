import json
import pathlib
from tqdm import tqdm
import nltk

nltk.download("stopwords")

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"
json_folder = resources_folder / "json"

input_json = json_folder / "id_to_category_list.json"  # Changed input to the output of step 1
output_json = json_folder / "category_to_id_list.json"  # New output file

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


