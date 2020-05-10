import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#what site
my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'
#open connection and get page
uClient = uReq(my_url)
page_html = uClient.read()
#close connection
uClient.close()
#parse the page
page_soup = soup(page_html, "html.parser")
#grabs each
containers = page_soup.findAll("div",{"class":"item-container"})
#file
filename = "products.csv"
f = open(filename, "w")
headers = "brand, product_name, shipping, price\n"
f.write(headers)
#retreive information
for container in containers:
    brands = container.findAll("a",{"class":"item-brand"})
    brand = brands[0].img["title"]
    
    titles = container.findAll("a",{"class":"item-title"})
    title = titles[0].text
    
    ships = container.findAll("li",{"class":"price-ship"})
    shipping = ships[0].text.strip()

    costs = container.findAll("li",{"class":"price-current"})
    cost1 = costs[0].strong.text
    cost1 = cost1.replace(',','')
    cost1 = int(cost1)
    cost2 = float(costs[0].sup.text)
    
    cost = cost1+cost2
    cost = str(cost)
    
    f.write(brand + "," + title.replace(","," ") + "," + shipping + "," + cost + "\n")

f.close()
