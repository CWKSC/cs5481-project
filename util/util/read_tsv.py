import pandas as pd

def read_tsv(tsv_file_path: str) -> pd.DataFrame:
    with open(tsv_file_path, "r", encoding="utf-8") as file:
        return pd.read_csv(
            file,
            delimiter="\t",
            header=None,
            names=["id", "title", "image_url", "upvotes", "comments"],
        )
