from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import pathlib
import time
import os

# Set GPU: 0 / 1 / 2 / 3
# nvidia-smi to check GPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

current_folder = pathlib.Path(__file__).parent
output_folder = current_folder / "text_category_intern_vl_2"
images_folder = current_folder / "images"

prompt = """Tag the image with categories, tag can be more than one, not too many, separated by commas"""

model = "OpenGVLab/InternVL2-8B"
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))

start_time = time.time()
for image_path in images_folder.iterdir():
    path = image_path.resolve().as_posix()
    image = load_image(path)
    response = pipe((prompt, image))
    print(response.text)
    with open(f"{output_folder}/{image_path.stem}.txt", "w") as f:
        f.write(response.text)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")

# Time taken: 4.29 seconds
