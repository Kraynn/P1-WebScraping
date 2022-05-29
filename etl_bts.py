from bs4 import BeautifulSoup
import requests
import csv
import re

def load_data(data,filename):
    with open(f"{filename}.csv", "a", newline="") as f:
        write = csv.writer(f)
        header = ['title', 'category', 'product_page_url', 'upc','price_including_tax',
        'price_excluding_tax','product_description', 'number_available', 'review_rating', 'image_url']
        write.writerow(header)
        write.writerows(data)

def parse_product(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') 
                                  
    title = soup.find('h1').text                                            
    img = soup.find("img").get("src")
    img = "https://books.toscrape.com" + img[5:]                                                            
    summary = soup.select("article[class=product_page]>p")                 
    rating = soup.find(class_=re.compile("star-rating.*"))                  
    rating = rating.get_attribute_list("class")[1]
    price = soup.find('p', class_="price_color").text
    price_tax = price                                                        
    upc = soup.find("td").text                                              
    cat = soup.find("ul", class_="breadcrumb")                              
    cat = cat.find_next("a")
    cat = cat.find_next("a")
    category = cat.find_next("a").text
    stock = soup.find("p", class_="instock availability").get_text().strip()        

    return (title, category, url, upc, price, price_tax, summary, stock, rating, img)
    
def browse_category(category):
    page = requests.get(category["url"])
    soup = BeautifulSoup(page.content, 'html.parser')

    product_data = []
    for url in soup.select("div[class=image_container]>a"):
        base_url = "https://books.toscrape.com/catalogue/"
        _url = url.get("href")
        _url = re.sub("^[../]+", base_url, _url)
        parsed_url = parse_product(_url)                              
        product_data.append(parsed_url)
    load_data(product_data,category["name"])

index = "http://books.toscrape.com/index.html"
page = requests.get(index)
soup = BeautifulSoup(page.content, 'html.parser')

categories = []
for cat_url in soup.select("li a[href*=category]"):
    base_index = "https://books.toscrape.com/"
    name = cat_url.text.strip()  
    category = {"name":name, "url":base_index+cat_url.get("href")}
    categories.append(category)                                          
categories.pop(0)

for category in categories:
    browse_category(category)
    
    npages = []
    page = requests.get(category["url"])
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.find(class_=re.compile("next.*")):
        pass
    for page_url in soup.select("li[class=next] a"):
        npage = re.sub("index.html", page_url.get("href"), category["url"])
        name = soup.find("h1").text
        category = {"name": name, "url": npage}
        npages.append(category)
        for npage in npages:
            browse_category(npage)

