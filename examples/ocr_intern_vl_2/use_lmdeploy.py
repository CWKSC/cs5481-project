from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import pathlib
import time

current_folder = pathlib.Path(__file__).parent
path = (current_folder / "jsid-post-a0eK0bq.png").resolve().as_posix()

model = "OpenGVLab/InternVL2-2B"
image = load_image(path)
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))


start_time = time.time()
response = pipe(("describe this image", image))
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")
print(response.text)

# Time taken: 4.36 seconds
# The image is a humorous meme that contrasts two different reactions to a news story. The meme is divided into two sections, each with a caption and a photo of a person reacting to the news.

# **Left Section:**
# - Caption: "TRANS SHOOTER MANIFESTO:"
# - Photo: A person with glasses, wearing a brown shirt, appears shocked and surprised.
# - Caption: "DO: 'CLASSIFIED! NO ONE CAN SEE IT.'"

# **Right Section:**
# - Caption: "TRUMP ASSASSIN LETTER OFFERING 150K TO WHOEVER FINISHES THE JOB:"
# - Photo: A person with glasses, wearing a red shirt, appears shocked and surprised.
# - Caption: "DO: 'CALL THE MEDIA! THE WORLD MUST SEE THIS!'"
