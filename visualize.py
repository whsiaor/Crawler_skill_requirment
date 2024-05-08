import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class Visualize:
    file = "ranking.csv"

    @classmethod
    def bar(cls):
        df = pd.read_csv(cls.file)

        key = df["Keyword"]
        value = df["Frequency"]

        fig, ax = plt.subplots(figsize=(len(key), 15))
        plt.bar(x=key, height=value)

        plt.savefig("bar_v.png")


    @classmethod
    def bar_h(cls):
        df = pd.read_csv(cls.file)

        key = df["Keyword"]
        value = df["Frequency"]

        fig, ax = plt.subplots(figsize=(10, len(key) / 4))
        plt.barh(y=key, width=value)
        plt.gca().invert_yaxis()
        plt.savefig("bar_h.png")


    @classmethod
    def cloud(cls):
        df = pd.read_csv(cls.file)
        key = df["Keyword"]
        value = df["Frequency"]

        word_freq_dict = dict(zip(key, value))
        wordcloud = WordCloud(width=1800, height=1600, background_color='white').generate_from_frequencies(word_freq_dict)

        plt.figure(figsize=(18, 16))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig("wordcloud.png", bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    ...
