import pathlib
from wordcloud import WordCloud

current_folder = pathlib.Path(__file__).parent
file_path = current_folder / "jsid-post-a0eKGed.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

wordcloud = WordCloud(width=1024, height=1024, background_color="white").generate(text)

wordcloud.to_file(current_folder / "wordcloud.png")
