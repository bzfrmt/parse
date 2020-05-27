from lxml import html
from lxml import etree
from pprint import pprint
import requests
import re
import time

def getmailru(limit):
    news=[]
    header= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    response = requests.get('https://news.mail.ru/rss/', headers = header)
    if response.ok:
        #print (response.text)
        #tree = etree.XML(response.text)
        s=response.text.encode('utf-8')
        dom = etree.fromstring(s, parser=etree.XMLParser(encoding='utf-8'))
        blocks = dom.xpath("//item")
        i = 0
        for block in blocks:
            if i<limit:
                data = {}
                data['link'] = block.xpath('.//link/text()')[0]
                data['date'] = block.xpath(".//pubDate/text()")[0]

                responsenews = requests.get(data['link'], headers = header)
                if responsenews.ok:
                    #print (responsenews.text)
                    domnews = html.fromstring(responsenews.text)
                    data['author']=domnews.xpath("//meta[@name='mediator_author']/@content")[0]
                    data['title']=domnews.xpath("//meta[@property='og:title']/@content")[0]
                news.append(data)
                time.sleep(1)
            i=i+1
    #pprint(news)

    return news

def getlentaru(limit):
    news=[]
    header= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    response = requests.get('https://lenta.ru/rss', headers = header)
    if response.ok:
        #print (response.text)
        #tree = etree.XML(response.text)
        s=response.text.encode('utf-8')
        dom = etree.fromstring(s, parser=etree.XMLParser(encoding='utf-8'))
        blocks = dom.xpath("//item")
        i = 0
        for block in blocks:
            if i<limit:
                data = {}
                data['link'] = block.xpath('.//link/text()')[0]
                data['date'] = block.xpath(".//pubDate/text()")[0]
                data['title'] = block.xpath('.//link/text()')[0]
                data['author'] = 'Lenta.ru'
                news.append(data)
            i=i+1
    #pprint(news)

    return news


def getyandexnews(limit):
    news=[]
    header= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    response = requests.get('https://yandex.ru/news/', headers = header)
    if response.ok:
        #print (response.text)
        blocks = re.findall('<a[^>]*(\/news\/story\/[^>"\/]+\-\-[^>"\/]+)\?[^>]*>',response.text)
        b=[]
        i = 0
        for block in blocks:
            if block not in b:
                if i<limit:
                    data = {}
                    data['link'] = 'https://yandex.ru' + block

                    responsenews = requests.get(data['link'], headers = header)
                    if responsenews.ok:
                    #    #print (responsenews.text)
                        domnews = html.fromstring(responsenews.text)
                        data['author']=domnews.xpath("//a[contains(@class,'agency-name')]/text()")[0]
                        data['title']=domnews.xpath("//meta[@property='og:title']/@content")[0]
                        #
                        data['date']=time.ctime(int(domnews.xpath("//meta[@property='og:updated_time']/@content")[0]))
                        #title = re.search('<a[^>]*agency\-name[^>]*>([^>]+)<\/a>',responsenews.text)
                        #if title:
                            #data['author']=title[1]

                    news.append(data)
                    time.sleep(1)
                i=i+1
            b.append(block)
    #pprint(news)

    return news

news1=getyandexnews(5)

news2=getlentaru(5)

news3=getmailru(5)

news=news1+news2+news3

pprint(news)


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///news.db',echo=True)
Base = declarative_base()

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String)
    link = Column(String)
    author = Column(String)
    date = Column(String)

    def __init__(self,  title, link, author, date):
        self.title = title
        self.link = link
        self.author = author
        self.date = date


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

for vac in news:
    countvac = session.query(News).filter(News.link == vac['link']).count()
    if countvac == 0:
        session.add(News(vac['title'],vac['link'],vac['author'],vac['date']))
        print ('Добавляем новость ',vac['link'])
        session.commit()

session.close()

