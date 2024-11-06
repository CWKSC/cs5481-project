from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
import json
import nltk
import pathlib
import re
import string

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
category_folder = root_folder / "resources" / "json" / "category"

# Input and output
input_json = category_folder / "step0_id_to_category_text.json"
output_json = category_folder / "step1_id_to_category_list.json"

# Specific exclusions and transformations
specific_exclusions = ["#tags#", "text"]
specific_transformations = {"memes": "meme", "cats": "cat"}

# Download stopwords and lemmatizer
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")
lemmatizer = WordNetLemmatizer()

with open(input_json, "r") as file:
    data = json.load(file)

result = {}
for key, value in tqdm(data.items(), total=len(data)):

    # Lowercase
    value = value.lower()

    # Example shit:
    # "jsid-post-agm5x7K": "The image can be tagged with the following categories:\n\n- The Guardian\n- Teen\n- World Record\n- Hands and Feet\n- US\n- 2024\n- September 17\n- 11:00 PM\n- MST\n- 4 min read\n- News\n- Youth\n- Achievement",
    if ":" in value:
        value = value.split(":")[1]

    # Remove hyphens for incorrect format - point form
    value = value.replace("-", "")

    # Split the value by newline and comma
    values = re.split("\n|,", value)

    # Strip with space and punctuation
    values = map(lambda x: x.strip(), values)
    values = map(lambda x: x.strip(string.punctuation), values)

    # Remove empty strings
    values = filter(lambda x: x != "", values)

    # Remove duplicates
    values = list(set(values))

    # Extend the values by splitting them by spaces
    extended_values = list(map(lambda x: x.split(" "), values))
    for extended_value in extended_values:
        values.extend(extended_value)

    # Remove stopwords
    values = filter(lambda x: x not in stopwords.words("english"), values)

    # Remove specific exclusions like "#tags#"
    values = filter(lambda x: x not in specific_exclusions, values)

    # Apply specific transformations
    def apply_specific_transformations(x):
        if x in specific_transformations:
            return specific_transformations[x]
        return x

    values = map(apply_specific_transformations, values)

    # Reference: https://www.cnblogs.com/jclian91/p/9898511.html
    def get_wordnet_pos(tag: str):
        if tag.startswith("J"):
            return wordnet.ADJ
        elif tag.startswith("V"):
            return wordnet.VERB
        elif tag.startswith("N"):
            return wordnet.NOUN
        elif tag.startswith("R"):
            return wordnet.ADV
        else:
            return None

    # Lemmatize
    def lemmatize_word(word: str):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        wn_tag = get_wordnet_pos(tag)
        if wn_tag is None:
            return word
        return lemmatizer.lemmatize(word, wn_tag)

    values = map(lemmatize_word, values)

    # Remove duplicates again
    values = set(values)

    # Remove length >= 40
    values = filter(lambda x: len(x) < 40, values)

    result[key] = list(values)


with open(output_json, "w") as file:
    json.dump(result, file, indent=4)
