from util.core.data_storage import read_data_grid
import pathlib

current_folder = pathlib.Path(__file__).parent
file_path = current_folder.parent.parent / "resources" / "bin" / "9gag-memes-llama-description-7k.bin"

df = read_data_grid(file_path)
print(df.posts[0].content)


