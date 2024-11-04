from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import pathlib
import time

current_folder = pathlib.Path(__file__).parent
image_path = (current_folder / "jsid-post-a0eK0bq.png").resolve()
path = image_path.as_posix()

model = "OpenGVLab/InternVL2-2B"
image = load_image(path)
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))

start_time = time.time()
response = pipe(("ocr, text only", image))
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")
print(response.text)

with open(f"{image_path.stem}.txt", "w") as f:
    f.write(response.text)

# Time taken: 1.25 seconds
# Trans shooter manifesto:
# "Do: 'Classified! No one can see it.'"

# Trump assassin letter offering 150K to whoever finishes the job:
# "Do: 'Call the media! The world must see this!'"

