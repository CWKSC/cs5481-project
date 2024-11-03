import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from util.read_tsv import read_tsv
import pathlib

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
tsv_file = root_folder / "resources" / "tsv" / "9gag-memes-dataset-stage1-10k.tsv"
images_folder = root_folder / "resources" / "images"

df = read_tsv(tsv_file)


# Download and save the image
def download_image(row):
    image_url = row["image_url"]
    id = row["id"]

    # Skip if the image is a video
    if image_url == "<video-content>":
        return

    # Download the image
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image.save(images_folder_path / f"{id}.png")
    except Exception as e:
        print(f"Error downloading {image_url}: {str(e)}")
        return None


# Loop through all image URLs and download images
for index, row in tqdm(df.iterrows(), total=len(df), desc="Downloading images"):
    download_image(row)
