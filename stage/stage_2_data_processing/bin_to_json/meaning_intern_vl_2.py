from util.core.data_storage import read_data_grid
import pathlib
import json

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"

bin_file_path = resources_folder / "bin" / "9gag-memes-intern-image-meaning.bin"
json_file_path = resources_folder / "json" / "meaning" / "id_to_meaning.json"

df = read_data_grid(bin_file_path)
post0 = df.posts[0]
print(post0.id)
print(post0.content)

result = {}
for post in df.posts:
    result[post.id] = post.content

with open(json_file_path, "w") as file:
    json.dump(result, file, indent=4)

