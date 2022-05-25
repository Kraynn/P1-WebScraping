from bs4 import BeautifulSoup
import requests
import urllib.request 

index = "http://books.toscrape.com/index.html"
page = requests.get(index)
soup = BeautifulSoup(page.content, 'html.parser')

def extract_img(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    img = soup.find("img").get("src")
    img = "https://books.toscrape.com" + img[5:]
    return(img)

def browse_product_url(categories_url):
    page = requests.get(categories_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    pictures = []
    for url in soup.select("div[class=image_container]>a"):
        base_url = "https://books.toscrape.com/catalogue/"
        _url = url.get("href")
        if _url[:9] == '../../../':
            _url = base_url + _url[9:]
        else:
            _url = base_url + _url[6:]

        img_data = extract_img(_url)                              
        pictures.append(img_data)

    for data in pictures:
        urllib.request.urlretrieve(data, f"{data[45:]}")
        
categories_url = []
for cat_url in soup.select("li a[href*=category]"):
    base_index = "https://books.toscrape.com/"
    categories_url.append(base_index+cat_url.get("href"))                                         
categories_url.pop(0)

for url in categories_url:
    browse_product_url(url)
