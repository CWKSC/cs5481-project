from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import pathlib
import time
from tqdm import tqdm

current_folder = pathlib.Path(__file__).parent
resources_folder = current_folder.parent.parent.parent / "resources"
images_folder = resources_folder / "images"
output_folder = resources_folder / "text_ocr_intern_vl_2"

existing_files = set(f.stem for f in output_folder.iterdir())

model = "OpenGVLab/InternVL2-8B"
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))

start_time = time.time()
for image_path in tqdm(images_folder.iterdir(), total=len(list(images_folder.iterdir())), desc="OCR by InternVL2-8B"):
    if image_path.stem in existing_files:
        continue
    path = image_path.resolve().as_posix()
    image = load_image(path)
    response = pipe(("ocr, text only", image))
    print(response.text)
    with open(f"{output_folder}/{image_path.stem}.txt", "w") as f:
        f.write(response.text)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")


