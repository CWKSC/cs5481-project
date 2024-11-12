import json
import pandas as pd
import pathlib

# Define the path to the JSON file
current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
sentiment_folder = root_folder / "resources" / "json" / "sentiment"
input_file = sentiment_folder / 'id_to_sentiment.json'  # Updated input file name

# Read the input JSON file
with open(input_file, 'r') as f:
    data = json.load(f)

# Prepare data for analysis
sentiment_scores = [value[0] for value in data.values()]  # Assuming sentiment score is the first element
upvotes = [value[1] for value in data.values()]  # Extracting upvotes directly from the second element

# Create a DataFrame for analysis
df = pd.DataFrame({
    'Sentiment Score': sentiment_scores,
    'Number of Upvotes': upvotes
})

# Categorize sentiment scores
df['Sentiment Category'] = pd.cut(df['Sentiment Score'],
                                   bins=[-float('inf'), -0.1, 0.1, float('inf')],
                                   labels=['Negative', 'Neutral', 'Positive'])

# Calculate standard deviation for each sentiment category
std_devs = df.groupby('Sentiment Category')['Number of Upvotes'].std()
mean_upvotes = df.groupby('Sentiment Category')['Number of Upvotes'].mean()

# Print standard deviations
print("Standard Deviations for Number of Upvotes:")
print(std_devs)
print("\nMean Number of Upvotes:")
print(mean_upvotes)