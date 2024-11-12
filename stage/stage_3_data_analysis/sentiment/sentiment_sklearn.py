import json
import pathlib
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from util.core.data_storage import read_data_grid
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Paths setup
current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"
sentiment_folder = root_folder / "resources" / "json" / "sentiment"

# Input
bin_file_path = resources_folder / "bin" / "9gag-memes-intern-image-meaning.bin"

# Output
output_file = sentiment_folder / "id_to_sentiment.json"

# Read data
df = read_data_grid(bin_file_path)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis
def analyze_sentiment(text):
    score = sia.polarity_scores(text)
    return score['compound']  # Return the compound score

# Function to filter text using TF-IDF
def clean_text(text: str, vectorizer: TfidfVectorizer) -> str:
    # Transform text to TF-IDF representation
    tfidf_matrix = vectorizer.transform([text])
    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    # Get the TF-IDF values
    tfidf_values = tfidf_matrix.toarray().flatten()
    # Filter words with non-zero TF-IDF scores
    filtered_tokens = [feature_names[i] for i in range(len(tfidf_values)) if tfidf_values[i] > 0]
    return " ".join(filtered_tokens)

def string_to_int(value: str) -> int:
    try:
        return int(value)
    except:
        try:
            return int(float(value[:-1]) * 1000) if value[-1].lower() == 'k' else 0
        except:
            # handle invalid upvote format with end with k
            return 0

# Prepare TF-IDF Vectorizer
corpus = [post.content for post in df.posts]
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(corpus)

# Perform sentiment analysis on each entry with progress bar
sentiment_results = {}
for post in tqdm(df.posts, desc="Analyzing Sentiment", unit="post"):
    cleaned_text = clean_text(post.content, vectorizer)
    sentiment_results[post.id] = [analyze_sentiment(cleaned_text), string_to_int(post.upvotes), post.comments]

# Write the results to an output JSON file
with open(output_file, 'w') as f:
    json.dump(sentiment_results, f, indent=4)

print("Sentiment analysis complete. Results saved to", output_file)