import json
import pathlib
import re
from tqdm import tqdm
import string
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"
json_folder = resources_folder / "json"

input_json = json_folder / "text_category_intern_vl_2.json"
output_json = json_folder / "id_to_category_list.json"

specific_exclusions = ["#tags#"]

with open(input_json, "r") as file:
    data = json.load(file)

result = {}
for key, value in tqdm(data.items(), total=len(data)):

    # Lowercase
    value = value.lower()

    # Example shit:
    # "jsid-post-agm5x7K": "The image can be tagged with the following categories:\n\n- The Guardian\n- Teen\n- World Record\n- Hands and Feet\n- US\n- 2024\n- September 17\n- 11:00 PM\n- MST\n- 4 min read\n- News\n- Youth\n- Achievement",
    if ":" in value:
        value = value.split(":")[1]

    # Remove hyphens for incorrect format - point form
    value = value.replace("-", "")

    # Split the value by newline and comma
    values = re.split("\n|,", value)

    # Strip with space and punctuation
    values = map(lambda x: x.strip(), values)
    values = map(lambda x: x.strip(string.punctuation), values)

    # Remove empty strings
    values = filter(lambda x: x != "", values)

    # Remove specific exclusions like "#tags#"
    values = filter(lambda x: x not in specific_exclusions, values)

    # Remove duplicates
    values = list(set(values))

    # Extend the values by splitting them by spaces
    extended_values = list(map(lambda x: x.split(" "), values))
    for extended_value in extended_values:
        values.extend(extended_value)

    # Remove stopwords
    values = filter(lambda x: x not in stopwords.words("english"), values)

    # Remove duplicates again
    values = set(values)

    # Remove length >= 40
    values = filter(lambda x: len(x) < 40, values)

    result[key] = list(values)


with open(output_json, "w") as file:
    json.dump(result, file, indent=4)
