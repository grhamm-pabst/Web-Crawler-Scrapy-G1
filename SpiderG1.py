import scrapy
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

url = "https://g1.globo.com/ultimas-noticias/"

uClient = uReq(url)
html = uClient.read()
uClient.close()

page_soup = soup(html, "html.parser")

containers = page_soup.findAll("div", {"class":"feed-post-body"})

for container in containers:
    title = container.findAll("a", {"class": "feed-post-link gui-color-primary gui-color-hover"})[0]
    description = container.findAll("div", {"class": "feed-post-body-resumo"})[0].text
    url_post = title["href"]
    img = container.findAll("img", {"class": "bstn-fd-picture-image"})[0]
    
    
    print("Titulo: {}".format(title.text))
    print("Descrição: {}".format(description))
    print("Link: {}".format(url_post))
    print("Imagem: {}".format(img["src"]))