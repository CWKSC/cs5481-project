import json
import matplotlib.pyplot as plt
import numpy as np
import pathlib

current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
sentiment_folder = root_folder / "resources" / "json" / "sentiment"

# Read the input JSON file
input_file = sentiment_folder / "id_to_sentiment.json"

with open(input_file, 'r') as f:
    data = json.load(f)

# Prepare data for analysis
sentiment_scores = [value[0] for value in data.values()]

# Bar chart for positive, negative, and neutral counts
positive_count = sum(1 for score in sentiment_scores if score > 0.1)
negative_count = sum(1 for score in sentiment_scores if score < -0.1)
neutral_count = len(sentiment_scores) - (positive_count + negative_count)

categories = ['Positive', 'Negative', 'Neutral']
counts = [positive_count, negative_count, neutral_count]

def autopct_with_category(pct, allvalues):
    absolute = int(np.round(pct / 100. * sum(allvalues)))
    return f'{absolute} ({pct:.1f}%)'


plt.figure(figsize=(8, 10))
plt.pie(counts, 
        labels=categories, 
        autopct=lambda pct: autopct_with_category(pct, counts), 
        startangle=90, 
        colors=['green', 'red', 'gray'])

plt.title('Sentiment Score Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.savefig('pie.png')  # Save the plot as an image