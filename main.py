
from constants import search_result_file
from get_vimrcs import get_vimrcs
import os
import pickle
import numpy as np
import pandas as pd

if not os.path.isfile(search_result_file):
    get_vimrcs(VERBOSE=True)

with open(search_result_file, "rb") as f:
    data = pickle.load(f)

vimrcs = pd.DataFrame(data)
a
def get_lines(vimrcs):
    for index, row in vimrcs.iterrows():
        print(row.url)
        lines = row.content.decode("UTF-8").split("\n")
        for line in lines:
            yield line

# Read each line into new dataframe
df = pd.DataFrame(get_lines(vimrcs), columns=["line"])

# Remove comment lines, inline comments, and extra whitespace

def remove_inline_comment(s):
    i = len(s) - 1
    while i >= 0:
        if s[i] == '"':
            return s[:i]
        i -= 1
    return s

df["line"] = df["line"].transform(remove_inline_comment)
df["line"] = df["line"].str.strip()
df = df[df["line"].str.startswith('"') == False]

# Filter out command words and blank lines
df = df[df["line"] != "endif"]
df = df[df["line"] != "endfunction"]
df = df[df["line"] != "else"]
df = df[df["line"] != ""]

# Filter by plugins, remove and place in new dataframe

# Clean plugins to remove "Plug" and whitespace

# Filter by mappings "nnoremap", etc., remove and place in new dataframe

# For each dataframe, count identical lines and sort by most frequent
line_counts = df \
    .pivot_table(index=["line"], aggfunc="size") \
    .sort_values(ascending=False)
print(line_counts.head(60))

# Other ideas:
# extract leader and local leader mappings
# In general, look up particular mappings
