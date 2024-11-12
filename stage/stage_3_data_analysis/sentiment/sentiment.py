import nltk
nltk.download('vader_lexicon')
nltk.download("words")
nltk.download("stopwords")
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import words
from util.core.data_storage import read_data_grid
import json
import pathlib
from tqdm import tqdm
import logging

words = set(words.words())
stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    tokens: list[str] = nltk.word_tokenize(text)
    filtered_tokens = []
    for word in tokens:
        if word in words and word not in stop_words:
            filtered_tokens.append(word)
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

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
resources_folder = root_folder / "resources"
sentiment_folder = root_folder / "resources" / "json" / "sentiment"

# Input
bin_file_path = resources_folder / "bin" / "9gag-memes-intern-image-meaning.bin"

# Output
output_file = sentiment_folder / "id_to_sentiment.json"

df = read_data_grid(bin_file_path)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis
def analyze_sentiment(text):
    score = sia.polarity_scores(text)
    return score['compound']  # Return the compound score

# Perform sentiment analysis on each entry with progress bar
sentiment_results = {}
for post in tqdm(df.posts, desc="Analyzing Sentiment", unit="post"):
    sentiment_results[post.id] = [analyze_sentiment(clean_text(post.content)), string_to_int(post.upvotes), post.comments]

# Write the results to an output JSON file
with open(output_file, 'w') as f:
    json.dump(sentiment_results, f, indent=4)

print("Sentiment analysis complete. Results saved to", output_file)