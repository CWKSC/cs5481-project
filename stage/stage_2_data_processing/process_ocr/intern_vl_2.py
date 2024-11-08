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

# Input
file_path = ocr_folder / "id_to_ocr_intern_vl_2.json"

# Output
output_file_path = ocr_folder / "id_to_ocr_token_list_intern_vl_2.json"

with open(file_path, "r", encoding="utf-8") as file:
    id_to_ocr_text = json.load(file)

words_list = words.words()
stop_words = set(stopwords.words("english"))

results = {}
for id, text in tqdm.tqdm(id_to_ocr_text.items(), desc="Clean OCR text"):
    if text == "":
        continue

    # Lowercase
    text = text.lower()

    # Tokenize
    tokens = nltk.word_tokenize(text)
    if len(tokens) == 0:
        continue

    # Filter by word in nltk.words
    tokens = filter(lambda word: word in words_list, tokens)

    # Remove stop words
    tokens = filter(lambda word: word not in stop_words, tokens)

    results[id] = list(tokens)

with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)
