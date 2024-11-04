import os
from PIL import Image
from typing import List, Set
from transformers import AutoProcessor, AutoModelForPreTraining
from transformers.models.mllama.processing_mllama import MllamaProcessor
from transformers.models.mllama.modeling_mllama import MllamaForConditionalGeneration
import pathlib
import time

os.environ["HF_TOKEN"] = "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"

current_folder = pathlib.Path(__file__).parent
images_folder = current_folder / "images"

model_id = "unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit"
processor: MllamaProcessor = AutoProcessor.from_pretrained(model_id)
model: MllamaForConditionalGeneration = AutoModelForPreTraining.from_pretrained(model_id)

prompt = f"<|image|><|begin_of_text|>Describe the image"

start_time = time.time()
for image_path in images_folder.iterdir():
    path = image_path.resolve().as_posix()
    image = Image.open(path)
    inputs = processor(image, prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=200)
    output = processor.decode(output[0])
    print(output)
    with open(f"meaning_llama_3_2_vision/{image_path.stem}.txt", "w") as f:
        f.write(output)

end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")

# Time taken: 55.30767369270325 seconds
