from bs4 import BeautifulSoup
import requests
import csv
import re
import csv

with open("Travel.csv", "w", newline="") as f:
        header = ['title', 'category', 'product_page_url', 'upc','price_including_tax', 'price_excluding_tax','product_description', 'number_available', 'review_rating', 'image_url']
        write = csv.writer(f)
        write.writerow(header)


def extract_data(data):
    rows = data
    with open("Travel.csv", "a", newline="") as f:
        write = csv.writer(f)
        write.writerow(rows)

def parse(url):
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
    

    stock = soup.find("p", class_="instock availability").get_text()        

    return (title, category, url, upc, price, price_tax, summary, stock, rating, img)
    
def browse_product_url(categories_url):

    page = requests.get(categories_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    product_data = []

    for url in soup.select("div[class=image_container]>a"):
        base_url = "https://books.toscrape.com/catalogue/"
        _url = url.get("href")
        
        if _url[:9] == '../../../':
            _url = base_url + _url[9:]
        else:
            _url = base_url + _url[6:]
       
        parsed_url = parse(_url)                              
        product_data.append(parsed_url)

    for data in product_data:
        extract_data(data)


index = "http://books.toscrape.com/index.html"
page = requests.get(index)
soup = BeautifulSoup(page.content, 'html.parser')

categories_url = []
for cat_url in soup.select("li a[href*=category]"):
    base_index = "https://books.toscrape.com/"
    categories_url.append(base_index+cat_url.get("href"))                                         
categories_url.pop(0)

for url in categories_url[:1]:
    browse_product_url(url)


