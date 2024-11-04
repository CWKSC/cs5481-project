from PIL import Image
import pytesseract
from tqdm import tqdm
import pathlib

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
images_folder = root_folder / "resources" / "images"
output_folder = root_folder / "resources" / "text_ocr_tesseract"

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Read image from images folder
png_files = list(images_folder.glob("*.png"))  # Get all PNG files

# Convert images to OCR text
for png_file in tqdm(png_files, desc="Images to OCR text"):
    image = Image.open(png_file)
    ocr_text = pytesseract.image_to_string(image)
    ocr_text_file = output_folder / f"{png_file.stem}.txt"
    ocr_text_file.write_text(ocr_text, encoding="utf-8")

