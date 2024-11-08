from nltk.corpus import stopwords, words
from wordcloud import WordCloud
import json
import nltk
import pathlib
import tqdm
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from wordcloud import ImageColorGenerator

nltk.download("stopwords")
nltk.download("words")

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
ocr_folder = root_folder / "resources" / "json" / "ocr"
mask_folder = current_folder / "mask"
results_folder = current_folder / "results"

# Input
file_path = ocr_folder / "id_to_ocr_token_list_tesseract.json"
mask_file_path = mask_folder / "rick_roll_mask.png"

# Output
output_file_path = results_folder / "ocr_tesseract_wordcloud.png"
output_file_color_path = results_folder / "ocr_tesseract_wordcloud_color.png"

mask_color = np.array(Image.open(mask_file_path))

# Transform mask to black and white
mask_bw = cv2.cvtColor(mask_color, cv2.COLOR_BGR2GRAY)

# Filter to black and white
mask_bw = np.where(mask_bw > 150, 255, 0)

# Save mask
cv2.imwrite(mask_folder / "rick_roll_mask_bw.png", mask_bw)

with open(file_path, "r", encoding="utf-8") as file:
    id_to_ocr_token_list = json.load(file)

# Join all the tokens
values = list(id_to_ocr_token_list.values())
text = " ".join(" ".join(token_list) for token_list in values)

wordcloud = WordCloud(
    background_color="white",
    mask=mask_bw,
).generate(text)
wordcloud.to_file(output_file_path)

image_colors = ImageColorGenerator(mask_color)
plt.figure(figsize=[50, 50])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

# store to file
plt.savefig(output_file_color_path, format="png")

# plt.show()
