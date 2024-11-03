from util.read_tsv import read_tsv
import pathlib

current_folder = pathlib.Path(__file__).parent
file_path = current_folder.parent.parent / "resources" / "tsv" / "9gag-memes-dataset-stage1-10k.tsv"

df = read_tsv(file_path)
print(df.head())

#                   id                                              title  ... upvotes comments
# 0  jsid-post-aPAYX5Q  Would you be able to hold her down ? Linguisti...  ...      55       13
# 1  jsid-post-aO8Y1LN                           Ruins the family reunion  ...      67        4
# 2  jsid-post-an79D65                The Crown is proud of the colonies.  ...      25       12
# 3  jsid-post-a5QMj3q                        Geologist hits rock bottom.  ...     122        3
# 4  jsid-post-aE02XOG                                    HoMM3 meme day!  ...     421       43

# [5 rows x 5 columns]
