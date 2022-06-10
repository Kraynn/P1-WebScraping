from bs4 import BeautifulSoup
import requests
import csv
import re

def load_data(data,filename, writeheader = False):
    with open(f"{filename}.csv", "a", newline="", encoding='utf-8') as f:
        write = csv.writer(f)
        header = ['title', 'category', 'product_page_url', 'upc','price_including_tax',
        'price_excluding_tax','product_description', 'number_available', 'review_rating', 'image_url']
        if writeheader:
            write.writerow(header)
        write.writerows(data)

def parse_product(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') 
                                  
    title = soup.find('h1').text                                            
    img = soup.find("img").get("src")
    img = "https://books.toscrape.com" + img[5:]       
    summary = ""                                                     
    for summary in soup.select("article[class=product_page]>p"):
        summary = summary.text
    if summary == "":
        summary = "Pas de description"                 
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
    
def browse_category(category, writeheader = False):
    page = requests.get(category["url"])
    soup = BeautifulSoup(page.content, 'html.parser')
    print(category)

    product_data = []
    for url in soup.select("div[class=image_container]>a"):
        base_url = "https://books.toscrape.com/catalogue/"
        _url = url.get("href")
        _url = re.sub("^[../]+", base_url, _url)
        parsed_url = parse_product(_url)                              
        product_data.append(parsed_url)
    load_data(product_data,category["name"], writeheader)

    if soup.find(class_=re.compile("next.*")):
        page_url = soup.select("li[class=next] > a")[0]
        npage = re.sub("index.html|page-([1-9]).html", page_url.get("href"), category["url"])
        newpage = {"name": category["name"], "url": npage}
        browse_category(newpage, writeheader = False)

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

for category in categories[2:]:
    browse_category(category, writeheader = True)
    
