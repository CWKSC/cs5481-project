from nltk.corpus import stopwords, words
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

current_folder = pathlib.Path(__file__).parent.resolve()
root_folder = current_folder.parent.parent.parent
meaning_folder = root_folder / "resources" / "json" / "meaning"

# Input
input_json = meaning_folder / "id_to_meaning.json"

# Output
output_file = meaning_folder / "id_to_meaning_list_tf_idf.json"

# Read input json
with open(input_json, "r", encoding="utf-8") as file:
    json_dict = json.load(file)

# Process
key_pair_list = list(json_dict.items())
key_pair_list.sort(key=lambda x: x[0])

content_list = [value for _, value in key_pair_list]
text_ids = [key for key, _ in key_pair_list]

# TF-IDF
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

# Show distribution
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


threshold = 0.05
result = {}
for i, id in enumerate(text_ids):
    tf_idf = tfidf_df.loc[id]
    tf_idf = tf_idf[tf_idf != 0]
    tf_idf = tf_idf[tf_idf > threshold]
    mean = tf_idf.mean()
    tf_idf = tf_idf[tf_idf >= mean]
    result[id] = tf_idf.index.tolist()

# Save to file
with open(output_file, "w") as file:
    json.dump(result, file, indent=4)
