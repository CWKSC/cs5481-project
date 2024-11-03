from util.read_tsv import read_tsv
import pathlib

current_folder = pathlib.Path(__file__).parent
file_path = current_folder.parent.parent / "resources" / "tsv" / "9gag-memes-dataset-stage1-10k.tsv"

df = read_tsv(file_path)
print(df.head())

#                   id                                              title                                          image_url upvotes comments
# 0  jsid-post-aPAYX5Q  Would you be able to hold her down ? Linguisti...  https://img-9gag-fun.9cache.com/photo/aPAYX5Q_...      55       13
# 1  jsid-post-aO8Y1LN                           Ruins the family reunion  https://img-9gag-fun.9cache.com/photo/aO8Y1LN_...      67        4
# 2  jsid-post-an79D65                The Crown is proud of the colonies.  https://img-9gag-fun.9cache.com/photo/an79D65_...      25       12
# 3  jsid-post-a5QMj3q                        Geologist hits rock bottom.  https://img-9gag-fun.9cache.com/photo/a5QMj3q_...     122        3
# 4  jsid-post-aE02XOG                                    HoMM3 meme day!  https://img-9gag-fun.9cache.com/photo/aE02XOG_...     421       43

