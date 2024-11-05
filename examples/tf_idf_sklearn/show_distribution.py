from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pathlib
import json
import matplotlib.pyplot as plt

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent
resources_folder = root_folder / "resources"

json_description_llama_3_2_vision = resources_folder / "json" / "text_description_llama_3_2_vision.json"
output_file = current_folder / "tf_idf_text_description_llama_3_2_vision.json"

with open(json_description_llama_3_2_vision, "r", encoding="utf-8") as file:
    text_dict = json.load(file)

key_pair_list = list(text_dict.items())
key_pair_list.sort(key=lambda x: x[0])

content_list = [value for _, value in key_pair_list]
text_ids = [key for key, _ in key_pair_list]

# input{'filename', 'file', 'content'}, default='content'
# If 'filename', the sequence passed as an argument to fit is expected to be a list of filenames that need reading to fetch the raw content to analyze.
# If 'file', the sequence items must have a ‘read’ method (file-like object) that is called to fetch the bytes in memory.
# If 'content', the input is expected to be a sequence of items that can be of type string or byte.
tfidf_vectorizer = TfidfVectorizer(input='content', stop_words='english')
tfidf_vector = tfidf_vectorizer.fit_transform(content_list)

tfidf_df = pd.DataFrame(
    tfidf_vector.toarray(), 
    index=text_ids, 
    columns=tfidf_vectorizer.get_feature_names_out()
)

print(tfidf_df)

data = tfidf_vector.toarray().flatten()
data = data[data > 0]

plt.figure(figsize=(10, 6))
plt.hist(data, bins=100, color='blue', alpha=0.7)
plt.title('TF-IDF Score Distribution')
plt.xlabel('TF-IDF Score')
plt.ylabel('Frequency')
plt.yscale('log')
plt.grid(True)
plt.show()