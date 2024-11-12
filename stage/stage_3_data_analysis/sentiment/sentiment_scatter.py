import json
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

# Define the path to the JSON file
current_folder = pathlib.Path(__file__).parent
root_folder = current_folder.parent.parent.parent
sentiment_folder = root_folder / "resources" / "json" / "sentiment"
input_file = sentiment_folder / 'id_to_sentiment.json'

# Read the input JSON file
with open(input_file, 'r') as f:
    data = json.load(f)

# Prepare data for analysis
sentiment_scores = [value[0] for value in data.values()]
upvotes = [value[1] for value in data.values()]

# Create a DataFrame for analysis
df = pd.DataFrame({
    'Sentiment Score': sentiment_scores,
    'Number of Upvotes': upvotes
})

# Categorize sentiment scores
df['Sentiment Category'] = pd.cut(df['Sentiment Score'],
                                   bins=[-float('inf'), -0.1, 0.1, float('inf')],
                                   labels=['Negative', 'Neutral', 'Positive'])

# Calculate the average number of upvotes
average_upvotes = df['Number of Upvotes'].mean()

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

# Define colors for each category
colors = {'Negative': 'red', 'Neutral': 'gray', 'Positive': 'green'}

# Create scatter plots for each category
for ax, category in zip(axs, ['Negative', 'Neutral', 'Positive']):
    subset = df[df['Sentiment Category'] == category]
    ax.scatter(subset['Number of Upvotes'], subset['Sentiment Score'], 
               color=colors[category], alpha=0.6, edgecolors='w')
    ax.set_title(f'{category} Sentiment')
    ax.set_xlabel('Number of Upvotes')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Add a horizontal line at y=0
    ax.axvline(average_upvotes, color='blue', linestyle='--', linewidth=1, label='Average Upvotes')  # Average upvotes line
    ax.grid()

# Set the y-label for the shared y-axis
axs[0].set_ylabel('Sentiment Score')

# Adjust layout
plt.tight_layout()
plt.savefig('scatter.png')  # Save the plot as an image