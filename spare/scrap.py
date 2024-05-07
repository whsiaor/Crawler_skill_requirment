import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm


def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    base_url = "https://www.seek.com.au"
    param = "/junior-developer-jobs?page={}"

    total_pages = 20

    with tqdm(total=total_pages, desc="Progress", leave=False) as pbar:  # 创建总体进度条
        for page in range(1, total_pages + 1):
            url = param.format(page)
            links = search_pages(base_url, url, headers)
            job_pages(base_url, links)
            pbar.update(1)  # 更新进度条
    


def search_pages(base_url, param, headers):
    url = base_url + param

    try:
        response = requests.get(url, headers=headers)
    
    except requests.exceptions.RequestException:
        print("Can't get urls")
    
    soup = BeautifulSoup(response.text, 'lxml')

    patten = re.compile(r'job-title-\d+')
    urls = soup.find_all("a", id=patten)

    links = [url.get("href") for url in urls]
    if len(links) < 1:
        print("No links")

    return links


def job_pages(base_url, links):
    for link in links:

        url = base_url + link

        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        details = soup.find('div', {'data-automation': 'jobAdDetails'})
        l = details.find_all('li') 
        
        with open('zz.txt', 'a') as file:
            for row in l:
                row = re.sub(r'[,.?!]$', '', row.text.strip())
                file.write(row + '\n')
    

main()
