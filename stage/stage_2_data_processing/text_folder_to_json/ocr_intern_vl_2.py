import pathlib
import json

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"

text_folder_path = resources_folder / "text_ocr_intern_vl_2"
json_file_path = resources_folder / "json" / "ocr" / "id_to_ocr_text_intern_vl_2.json"

result = {}
for file in text_folder_path.glob("*.txt"):
    result[file.stem] = file.read_text(encoding="utf-8")

with open(json_file_path, "w", encoding="utf-8") as file:
    json.dump(result, file, indent=4)

