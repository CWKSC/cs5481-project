from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import pathlib
import time

current_folder = pathlib.Path(__file__).parent
images_folder = current_folder / "images"

model = "OpenGVLab/InternVL2-8B"
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))

prompt = """Tag the image with categories, tag can be more than one, not too many, separated by commas"""

start_time = time.time()
for image_path in images_folder.iterdir():
    path = image_path.resolve().as_posix()
    image = load_image(path)
    response = pipe((prompt, image))
    print(response.text)
    with open(f"category_intern_vl_2/{image_path.stem}.txt", "w") as f:
        f.write(response.text)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")

# Time taken: 4.29 seconds
