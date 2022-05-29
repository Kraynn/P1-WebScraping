from bs4 import BeautifulSoup
import requests
import urllib.request 
import re

index = "http://books.toscrape.com/index.html"
page = requests.get(index)
soup = BeautifulSoup(page.content, 'html.parser')

def extract_img(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    img = soup.find("img").get("src")
    img = "https://books.toscrape.com" + img[5:]

    return(img)

def browse_category(category):

    page = requests.get(category)
    soup = BeautifulSoup(page.content, 'html.parser')

    pictures = []
    for url in soup.select("div[class=image_container]>a"):
        base_url = "https://books.toscrape.com/catalogue/"
        _url = url.get("href")
        _url = re.sub("^[../]+", base_url, _url)
        img_data = extract_img(_url)                              
        pictures.append(img_data)

    for data in pictures:
        urllib.request.urlretrieve(data, f"{data[45:]}")
        
categories = []
for cat_url in soup.select("li a[href*=category]"):
    base_index = "https://books.toscrape.com/"
    categories.append(base_index+cat_url.get("href"))                                         
categories.pop(0)

for url in categories[:2]:
    browse_category(url)
    npages = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.find(class_=re.compile("next.*")):
        pass
    for page_url in soup.select("li[class=next] a"):
        npage = re.sub("index.html", page_url.get("href"), url)
        npages.append(npage)
        for npage in npages:
            browse_category(npage)

