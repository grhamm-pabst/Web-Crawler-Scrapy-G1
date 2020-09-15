import scrapy
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from time import sleep
from pymongo import MongoClient

url = "https://g1.globo.com/ultimas-noticias/"

class News:
    def __init__(self, title, desc, url, img):
        super().__init__()
        self.title = title
        self.desc = desc
        self.url = url
        self.img = img
        


try:
    mongo = MongoClient('localhost', 27017)
    db = mongo.G1News
    latest_news = db.g1news
except:
    print('Não Foi possivel conectar ao mongo')

while True:
    
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    

    page_soup = soup(html, "html.parser")

    containers = page_soup.findAll("div", {"class":"feed-post-body"})
    
    
    for container in containers:
        
        try:
            try:
                title = container.findAll("a", {"class": "feed-post-link gui-color-primary gui-color-hover"})[0]
                url_post = title["href"]
            except:
                title = ""
                url_post = ""
            
            try:
                description = container.findAll("div", {"class": "feed-post-body-resumo"})[0].text
            except:
                description = ""
            
            try:
                img = container.findAll("img", {"class": "bstn-fd-picture-image"})[0]
                img = img["src"]
            except:
                img = ""
                
        
    
            news = News(title.text, description, url_post, img)
        
            
            
            news_up = {
                "title": news.title,
                "description": news.desc,
                "url": news.url,
                "img": news.img
            }
            doc = latest_news.find_one({"title":news_up["title"]})
            if doc == None:
                latest_news.insert_one(news_up)
            else:
                print("Sem noticias novas")
                break
                
            print("Titulo: {}".format(news.title))
            print("Descrição: {}".format(news.desc))
            print("Link: {}".format(news.url))
            print("Imagem: {}".format(news.img))
            
        except:
            print("Algum elemento não encontrado!")
        
        title = ""
        description = ""
        url_post = ""
        img = ""
        
    sleep(20)
