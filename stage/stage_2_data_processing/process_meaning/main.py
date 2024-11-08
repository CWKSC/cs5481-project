from nltk.corpus import stopwords, words
import json
import nltk
import pathlib
import tqdm

nltk.download("stopwords")
nltk.download("words")

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
ocr_folder = root_folder / "resources" / "json" / "ocr"


