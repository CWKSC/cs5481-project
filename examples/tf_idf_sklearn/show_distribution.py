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
feature_names = tfidf_vectorizer.get_feature_names_out()

# TF (Term Frequency)
tf_vector = tfidf_vectorizer.transform(content_list)
tf_df = pd.DataFrame(tf_vector.toarray(), index=text_ids, columns=feature_names)

# IDF (Inverse Document Frequency)
idf_vector = tfidf_vectorizer.idf_
idf_df = pd.DataFrame(idf_vector, index=feature_names, columns=["IDF"])

# TF-IDF
tfidf_df = pd.DataFrame(
    tfidf_vector.toarray(), 
    index=text_ids, 
    columns=feature_names
)

data = tfidf_vector.toarray().flatten()
data = data[data > 0]

# TF Distribution
tf_data = tf_vector.toarray().flatten()
tf_data = tf_data[tf_data > 0]

plt.figure(figsize=(15, 6))

# TF Histogram
plt.subplot(1, 3, 1)
plt.hist(tf_data, bins=100, color='green', alpha=0.7)
plt.title('TF Score Distribution')
plt.xlabel('TF Score')
plt.ylabel('Frequency')
plt.grid(True)

# IDF Distribution
idf_data = idf_vector.flatten()

# IDF Histogram
plt.subplot(1, 3, 2)
plt.hist(idf_data, bins=100, color='orange', alpha=0.7)
plt.title('IDF Score Distribution')
plt.xlabel('IDF Score')
plt.ylabel('Frequency')
plt.grid(True)

# TF-IDF Histogram
plt.subplot(1, 3, 3)
plt.hist(data, bins=100, color='blue', alpha=0.7)
plt.title('TF-IDF Score Distribution')
plt.xlabel('TF-IDF Score')
plt.ylabel('Frequency')
plt.grid(True)

plt.tight_layout()
plt.show()

