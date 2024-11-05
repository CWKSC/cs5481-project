import pathlib
from nltk.corpus import stopwords
import nltk
import string
from nltk.corpus import words

nltk.download("stopwords")
nltk.download("punkt_tab")
nltk.download("words")

current_folder = pathlib.Path(__file__).parent
file_path = current_folder / "jsid-post-a0eKGed.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

print("Original:")
print(text)
print("===")

# Lowercase
text = text.lower()

# Tokenize
tokens = nltk.word_tokenize(text)
print("Tokens:")
print(tokens)
print(len(tokens))
print()

# Remove stop words
stop_words = set(stopwords.words("english"))
filtered_tokens = [word for word in tokens if word not in stop_words]

print("Removed stop words:")
print(filtered_tokens)
print(len(filtered_tokens))
print()

# Filter by word in nltk.words
filtered_tokens = [word for word in filtered_tokens if word in words.words()]

print("Final:")
print(filtered_tokens)
print(len(filtered_tokens))

with open("final.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filtered_tokens))

