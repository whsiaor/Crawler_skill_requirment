from bs4 import BeautifulSoup
from info import Spider
import pytest 
import os
import re

url = "https://www.seek.com.au/Developer-jobs" 

@pytest.fixture
def spider():
    return Spider()

def test_get_res(spider):
    response = spider.get_res(url)
    assert response.status_code == 200

def test_find_sub_urls(spider):
    sub_links = spider.find_sub_urls(url)
    assert isinstance(sub_links, list)
    assert len(sub_links) > 0

def test_keywords():
    skills = ['C', 'C++', 'C#', '.NET', 'Vue.js', 'Laravel', 'Hello World']
    keywords = []
    for skill in skills:
        matches = re.findall(r'\w*/?\s?\.?\w+#*\+*\s?\w*', skill)
        keywords.extend(matches)
    assert skills == keywords
 
def test_save_csv(spider):
    spider.save_csv()
    # Assert that the file exists
    assert os.path.exists(spider.file_name)

def test_crawl_pages(spider):
    total_pages = 2
    spider.crawl_pages(total_pages)
    # Assert that the file exists
    assert os.path.exists(spider.file_name)

def test_content():
    dsc = '<li>Passion for staying ahead of web development trends.</li>'
    soup = BeautifulSoup(dsc, 'html.parser')
    text = soup.get_text(strip=True)

    text = re.sub(r'[,.?!]$', '', text)
    assert text == 'Passion for staying ahead of web development trends'