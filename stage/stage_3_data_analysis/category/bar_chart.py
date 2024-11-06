import json
import pathlib
from tqdm import tqdm
import matplotlib.pyplot as plt  # New import for plotting

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"
json_folder = resources_folder / "json"

input_json = json_folder / "category_to_id_list.json"  # Input from step 2
top_n = 50

with open(input_json, "r") as file:
    data = json.load(file)

print(f"Number of categories: {len(data)}")

# New code to create a bar chart
# Count the number of IDs for each category
category_counts = {category: len(ids) for category, ids in data.items()}

# Find categories with only one ID
single_id_categories = [category for category, count in category_counts.items() if count == 1]
print(f"Number of categories with only one ID: {len(single_id_categories)}")

# Find categories with only two IDs
two_id_categories = [category for category, count in category_counts.items() if count == 2]
print(f"Number of categories with only two IDs: {len(two_id_categories)}")

# Find categories with only three IDs
three_id_categories = [category for category, count in category_counts.items() if count == 3]
print(f"Number of categories with only three IDs: {len(three_id_categories)}")

# Sort categories by count and get the top n
top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
categories, counts = zip(*top_categories)

# Create the bar chart
plt.figure(figsize=(12, 6))
plt.bar(categories, counts)
plt.xticks(rotation=45, ha='right')
plt.title(f'Top {top_n} Categories by ID Count')
plt.xlabel('Categories')
plt.ylabel('Number of IDs')
plt.tight_layout()
plt.show() 

