
from constants import search_result_file
from get_vimrcs import get_vimrcs
from plot import plot, generate_wordcloud
from get_lines import get_lines
import os
import pickle


# Search for vimrcs on GitHub if no existing search results are present
if not os.path.isfile(search_result_file):
    get_vimrcs(VERBOSE=True)

# Open search results
with open(search_result_file, "rb") as f:
    data = pickle.load(f)

# Get cleaned lines for each category
settings, maps, plugins, leaders = get_lines(data["all_vimrcs"])

# Create barplots for each category
plot(settings, threshold=50, filename="settings_barplot.jpg")
plot(maps, threshold=10, filename="maps_barplot.jpg")
plot(plugins, threshold=15, filename="plugins_barplot.jpg")
plot(leaders, threshold=4, filename="leaders_barplot.jpg")

# Create wordclouds for each category
generate_wordcloud(settings, filename="settings_wordcloud.jpg")
generate_wordcloud(plugins, filename="plugins_wordcloud.jpg")
