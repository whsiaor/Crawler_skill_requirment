import pandas as pd
from tqdm import tqdm
from collections import Counter
import re


counter = Counter()

with open("list.txt") as file:
    keywords = [word.strip() for word in file.read().replace('"', '').split(",")]

with open('content.txt') as file:
    lines = file.readlines()
    for line in tqdm(lines):
        words = re.sub(r'[^.?\w+*?#?\s]', '', line).split()
        for word in words:
            if word in keywords:
                counter[word] += 1



sorted_words = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))

df = pd.DataFrame(sorted_words.items(), columns=['Keyword', 'Frequency'])

file_name = "ranking.csv"
df.to_csv(file_name, index=False)
print(f'{file_name} is ready')