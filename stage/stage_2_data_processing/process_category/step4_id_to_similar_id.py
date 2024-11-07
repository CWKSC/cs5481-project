from tqdm import tqdm
import json
import math
import pathlib

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

# Input
category_to_id_list_json = category_folder / "step2_category_to_id_list.json"
id_to_category_list_json = category_folder / "step3_id_to_category_remove_uncommon.json"
id_to_category_list_top_30_json = category_folder / "step3_id_to_category_top_30.json"

# Output
id_to_similar_id_json = category_folder / "step4_id_to_similar_id.json"
id_to_similar_id_from_top_30_json = (
    category_folder / "step4_id_to_similar_id_from_top_30.json"
)

# Load data
with open(category_to_id_list_json, "r") as file:
    category_to_id_list = json.load(file)
with open(id_to_category_list_json, "r") as file:
    id_to_category_list = json.load(file)
with open(id_to_category_list_top_30_json, "r") as file:
    id_to_category_list_top_30 = json.load(file)

# Get IDF of each category
total_ids = len(id_to_category_list.keys())
print("Total ids:", total_ids)
idf = {}
for category, ids in category_to_id_list.items():
    idf[category] = math.log((total_ids + 1) / (len(ids) + 1), total_ids + 1)

# Sort idf by value
idf = dict(sorted(idf.items(), key=lambda item: item[1], reverse=True))
print(
    "First 5 idf:",
    ", ".join(
        [f"{category}: {value:.3f}" for category, value in list(idf.items())[:5]]
    ),
)
print(
    "Last 5 idf:",
    ", ".join(
        [f"{category}: {value:.3f}" for category, value in list(idf.items())[-5:]]
    ),
)

result = {}
for id, categories in tqdm(
    id_to_category_list.items(),
    total=len(id_to_category_list),
    desc="Get similarity of each id with idf",
):
    similarity = {}
    for other_id, other_categories in id_to_category_list.items():
        if id == other_id:
            continue

        # Get the number of categories that are the same between two ids
        intersection = set(categories) & set(other_categories)
        if len(intersection) == 0:
            continue

        # Calculate similarity value
        similarity_value = sum(idf[category] for category in intersection)

        similarity[other_id] = similarity_value

    # Keep only top 10 similar ids
    similarity = dict(
        sorted(similarity.items(), key=lambda item: item[1], reverse=True)[:10]
    )
    result[id] = similarity

# Save result
with open(id_to_similar_id_json, "w") as file:
    json.dump(result, file, indent=4)


result = {}
for id, categories in tqdm(
    id_to_category_list_top_30.items(),
    total=len(id_to_category_list_top_30),
    desc="Get similarity of each id from top 30 categories",
):
    similarity = {}
    for other_id, other_categories in id_to_category_list_top_30.items():
        if id == other_id:
            continue

        # Get the number of categories that are the same between two ids
        intersection = set(categories) & set(other_categories)
        if len(intersection) == 0:
            continue

        # Calculate similarity value
        similarity_value = sum(idf[category] for category in intersection)

        similarity[other_id] = similarity_value

    # Keep only top n similar ids
    similarity = dict(
        sorted(similarity.items(), key=lambda item: item[1], reverse=True)[:1400]
    )
    result[id] = similarity

# Save result
with open(id_to_similar_id_from_top_30_json, "w") as file:
    json.dump(result, file, indent=4)
