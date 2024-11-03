from PIL import Image
import pytesseract
import time
import pathlib

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

current_folder = pathlib.Path(__file__).parent
image_path = current_folder / "cow.jpg"
image = Image.open(image_path)

start_time = time.time()
extracted_text = pytesseract.image_to_string(image)
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")
print(extracted_text)

# Time taken: 0.34 seconds
# With cold weather on the way, cows
# will seek the warmth of car engines,
# make sure you check around properly
# before driving away.


