from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import pathlib
import json
import matplotlib.pyplot as plt
import numpy as np

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
print("TF:")
print(tf_df.head(3))

# IDF (Inverse Document Frequency)
idf_vector = tfidf_vectorizer.idf_
idf_df = pd.DataFrame(idf_vector, index=feature_names, columns=["IDF"])
print("IDF:")
print(idf_df.head(3))

# TF-IDF
tfidf_df = pd.DataFrame(
    tfidf_vector.toarray(), 
    index=text_ids, 
    columns=feature_names
)
print("TF-IDF:")
print(tfidf_df.head(3))

threshold = 0.5

result = {}
for i, id in enumerate(text_ids):
    tf_idf = tfidf_df.loc[id]
    tf_idf = tf_idf[tf_idf != 0]
    # if "image" in tf_idf.index:
    #     print(tf_idf)
    if id == "jsid-post-aXPxzVd":
        print("TF: ", tf_df.loc[id]["image"])
        print("IDF: ", idf_df.loc["image"])
        print("TF-IDF: ", tf_idf["image"])
    tf_idf = tf_idf[tf_idf > threshold]
    # mean = words.mean()
    # filtered_indices = words[words >= mean]
    result[id] = tf_idf.index.tolist()

# Save to file
with open(output_file, "w") as file:
    json.dump(result, file, indent=4)

