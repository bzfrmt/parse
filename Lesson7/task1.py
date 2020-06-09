from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

limitcount=2
limitpage=10

driver = webdriver.Chrome()

driver.get('https://account.mail.ru/login')
time.sleep(1)
elem = driver.find_element_by_name("username")

#elem = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,'username')))

#elem = driver.find_element_by_xpath("//input[@name='login']")
elem.send_keys('study.ai_172')

nextbutton = driver.find_element_by_xpath("//button[@data-test-id='next-button']")
actions = ActionChains(driver)
actions.move_to_element(nextbutton).click().perform()
time.sleep(2)
elem = driver.find_element_by_name("password")
#elem = driver.find_element_by_xpath("//input[@name='login']")
elem.send_keys('NextPassword172')

elem.send_keys(Keys.RETURN)
time.sleep(2)



assert "study.ai_172@mail.ru" in driver.find_element_by_xpath("//i[@id='PH_user-email']").text

print(driver.find_element_by_xpath("//i[@id='PH_user-email']").text)
time.sleep(5)
links ={}
lastid=''
for i in range(limitpage):
    time.sleep(1)
    articles = driver.find_elements_by_xpath("//a[contains(@class,'js-letter-list-item')]")
    if articles:
        for article in articles:
            links[article.get_attribute('data-uidl-id')]=article.get_attribute('href')


        actions = ActionChains(driver)
        actions.move_to_element(articles[-1])
        actions.perform()
        #print(len(articles))
        print(articles[-1].get_attribute('data-uidl-id'))
    if lastid==articles[-1].get_attribute('data-uidl-id'):
        break
    if articles:
        lastid=articles[-1].get_attribute('data-uidl-id')

    #driver.execute_script("window.scrollTo(0, 500)")
    #html = driver.find_element_by_tag_name('html')
    #html.send_keys(Keys.PAGE_DOWN)
#for link in links:
#    print (link,links[link])
print(len(links))

#exit()
#print (driver.page_source)
#blocks = re.findall('<a[^>]*href="([^>"]*inbox\/\d+\:\d+\:\d+\/[^>"]*)"[^>]*data\-uidl\-id="(\d+?)"[^>]*>',driver.page_source)
#links =[]
#links ={}
#if blocks:
#    print(len(blocks))
#    for block in blocks:
#        link={}
        #print (block[0], block[1])
#        links[block[1]]='https://e.mail.ru' + block[0]
        #links.append(link)


i=0
mails=[]
for link in links:
    print (link,links[link])
    driver.get(links[link])
    time.sleep(10)
    mail={}
    mail['link']=links[link]
    mail['key']=link
    mail['subject']=driver.find_element_by_xpath("//h2[contains(@class,'thread__subject')]").text
    mail['from']=driver.find_element_by_xpath("//span[@class='letter-contact']").get_attribute("title")
    mail['date']=driver.find_element_by_xpath("//div[@class='letter__date']").text
    #не понял как забрать отсюда html, а не текст
    mail['body']=driver.find_element_by_xpath("//div[@id='style_" + str(link) + "_BODY']").get_attribute('innerHTML')
    mails.append(mail)
    i=i+1
    if i>=limitcount:
        break


for mail in mails:
    print (mail)





from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///mails.db',echo=True)
Base = declarative_base()

class Mails(Base):
    __tablename__ = 'mails'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    key = Column(String)
    link = Column(String)
    subject = Column(String)
    author = Column(String)
    date = Column(String)
    body = Column(String)

    def __init__(self,  key, link, subject, author, date, body):
        self.key = key
        self.link = link
        self.subject = subject
        self.author = author
        self.date = date
        self.body = body


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

for vac in mails:
    countvac = session.query(Mails).filter(Mails.key == vac['key']).count()
    if countvac == 0:
        session.add(Mails(vac['key'],vac['link'],vac['subject'],vac['from'],vac['date'],vac['body']))
        print ('Добавляем письмо ',vac['key'])
        session.commit()

session.close()







# driver.quit()