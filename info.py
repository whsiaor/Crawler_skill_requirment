from collections import Counter
import re
import requests
from requests.exceptions import RequestException
from visualize import Visualize
import time
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        self.base_url = "https://www.seek.com.au"
        self.param = "/developer-jobs?page={}"
        self.total_pages = 20
        self.list = "list.txt"
        self.file_name = "ranking1.csv"
        self.counter = Counter()

    # get reques
    def get_res(self, url):
        max_retries = 3  # 最大重試次數
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                if response.status_code == 200:
                    return response
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print("Too many requests. Retrying after a delay...")
                    time.sleep(1)  # 在這裡增加一個延遲，例如10秒
                    retries += 1
                    continue
                else:
                    raise
            except RequestException :
                raise RequestException
            
        raise Exception("Failed to get response from the URL after multiple retries.")



    # Parse HTML data to find and extract sub URLs
    def find_sub_urls(self, url):

        response = self.get_res(url)
        soup = BeautifulSoup(response.text, 'lxml')

        patten = re.compile(r'job-title-\d+')
        urls = soup.find_all("a", id=patten)

        sub_urls = [url.get("href") for url in urls]

        if len(sub_urls) < 1:
            raise ValueError("No links found on the page")
        
        return sub_urls
    

    # Extract keywords from a text file
    def get_keywords(self):
        with open(self.list) as file:
            file = file.read()
            keywords = re.findall(r'\w*/? ?\.?\w+#*\+* ?\w*', file)
            return keywords
    

    # Process sub URLs 
    def to_sub_urls(self, sub_urls):
        for sub_url in tqdm(sub_urls, desc="Iterating description finding keywords", leave=False):
            self.in_sub_url(sub_url)


    # Lookup keywords in description and update counter
    def in_sub_url(self, sub_url):
        keywords = self.get_keywords() 
        # Go to page and finding description
        url = self.base_url + sub_url
        response = self.get_res(url)
        soup = BeautifulSoup(response.text, 'lxml')
        # Find the tag
        details = soup.find('div', {'data-automation': 'jobAdDetails'})
        text = details.find_all('li') 
        # Clean description
        text = [re.sub(r'[,.?!]$', '', li.text.strip()) for li in text]

        # Iterating description finding keywords
        found = set()
        for row in text:
            words = re.split(r'[\s!@$%^&*(),]', row)
            for word in words:
                if word in keywords:
                    found.add(word)
        for key in found:
            self.counter[key] += 1
 

    # Save keyword frequencies to a CSV file
    def save_csv(self):
        sorted_words = dict(sorted(self.counter.items(), key=lambda item: item[1], reverse=True))

        df = pd.DataFrame(sorted_words.items(), columns=['Keyword', 'Frequency'])
        df.to_csv(self.file_name, index=False)


    # Crawl all pages
    def crawl_pages(self, total=None, max_workers=3, delay=1):
        total_pages = self.total_pages if total is None else total
        with open(self.file_name, 'w') as file:
            pass
        
        for page in tqdm(range(1, total_pages + 1), desc="Total", leave=False):
            url = self.base_url + self.param.format(page)
            links = self.find_sub_urls(url)
            self.to_sub_urls(links)
            self.save_csv()


if __name__ == "__main__":

    spider = Spider()
    spider.crawl_pages() # Insert how many search pages you want to crawl for, defalt=20, every page got 22 links

    # Visualize.cloud() # Ouuput word cloud image
    # Visualize.bar() # Output bar chart 
