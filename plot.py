import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud


def transform(data, threshold):
    lines, counts = [], []
    for line, count in Counter(data).most_common():
        if line and count > threshold:
            lines.append(line)
            counts.append(count)
    return {"Settings": lines, "Frequency": counts}


def plot(lines, threshold, filename):

    # Transform data into plot-able format and cutoff below threshold
    data = transform(lines, threshold)

    # Get height
    height = max(len(data["Settings"]) / 4, 2)
    width = max(data["Frequency"]) / 2

    # Initialize the matplotlib figure
    sns.set_theme(style="whitegrid")
    f, ax = plt.subplots(figsize=(8, height))

    # Create barplot
    sns.barplot(y="Settings", x="Frequency", data=data, palette="pastel")

    # Add a legend labels
    f.subplots_adjust(left=0.4, bottom=0.3)
    ax.set(ylabel="Settings", xlabel="Frequency")
    sns.despine(left=True, bottom=True)

    # Save figure
    plt.savefig("figures/" + filename)


def generate_wordcloud(lines, filename):

    # Create wordcloud
    width, height = 8, 4
    wc = WordCloud(
        background_color="white",
        max_words=50,
        color_func=lambda *args, **kwargs: (50, 50, 50),
        width=width*100,
        height=height*100
    )
    wc.generate_from_frequencies(Counter(lines))

    # Save figure
    f, ax = plt.subplots(figsize=(width, height))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig("figures/" + filename)
