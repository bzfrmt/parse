from bs4 import BeautifulSoup as bs
import requests
import re
import urllib
from pprint import pprint
import pandas as pd
import numpy as np
searchtext='программер'
#searchtext=input("Введите ключевое слово: ")
maxpage=2
print (searchtext)


def gethh(searchtext,maxpage):
    nextpage = True
    npage=0
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
    serials = []
    while nextpage and npage<maxpage:
        print ('Страница:',npage)
        params = {}
        main_link = 'https://orenburg.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&search_field=name&text=' + searchtext + '&showClusters=true&page='+str(npage)

        response = requests.get(main_link,headers=header,params=params)

        if response.ok:
            soup = bs(response.text,'lxml')
            serials_list = soup.find_all('div',{'class':'vacancy-serp-item'})


            for serial in serials_list:
                serial_data = {}
                #<a class="bloko-link HH-LinkModifier" data-qa="vacancy-serp__vacancy-title" href="https://orenburg.hh.ru/vacancy/36995159?query=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82" data-position="50" data-requestid="1589999805908e5bc5352b182f0d4163" data-totalvacancies="15776" target="_blank">Программист IT фармкомпанию</a>
                #print(serial.find('a',{'class':'bloko-link HH-LinkModifier'}))
                serial_data['host'] = 'hh.ru'
                serial_data['link'] = serial.find('a',{'class':'bloko-link HH-LinkModifier'})['href']
                serial_data['name'] = serial.find('a',{'class':'bloko-link HH-LinkModifier'}).string
                #<span class="bloko-section-header-3 bloko-section-header-3_lite" data-qa="vacancy-serp__vacancy-compensation">от 150&nbsp;000 KZT</span>
                serial_data['compensation'] = None
                serial_data['minsalary'] = None
                serial_data['maxsalary'] = None
                serial_data['currency'] = None
                salary = {}
                #salary[1]=None
                #salary[2]=None
                #salary[3]=None
                if serial.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'}):
                    serial_data['compensation'] = serial.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'}).string.replace('\xa0','')
                    #print(serial_data['compensation'])
                    #salary=re.search("(?:от\s+(\d+)(\D*)\s+(\D+)|до\s+(\D*)(\d+)\s+(\D+)|(\d+)\s*\-\s*(\d+)\s+(\D+))", serial_data['compensation'])
                    salary=re.search("(\d+)\s*\-\s*(\d+)\s+(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[3],' min:',salary[1],'max:',salary[2])
                        serial_data['currency'] = salary[3]
                        serial_data['minsalary'] = salary[1]
                        serial_data['maxsalary'] = salary[2]

                    salary=re.search("от\s+(\d+)\s+(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[2],' min:',salary[1])
                        serial_data['currency'] = salary[2]
                        serial_data['minsalary'] = salary[1]

                    salary=re.search("до\s+(\d+)\s+(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[2],' max:',salary[1])
                        serial_data['currency'] = salary[2]
                        serial_data['maxsalary'] = salary[1]

                    salary=re.search("^(\d+)\s+(\D+)", serial_data['compensation'])
                    if salary:
                        print('val:',salary[2],' max:',salary[1])
                        serial_data['currency'] = salary[2]
                        serial_data['minsalary'] = salary[1]
                        serial_data['maxsalary'] = salary[1]
                print(serial_data)
                serials.append(serial_data)
            #pprint(serials)

            #<a class="bloko-button HH-Pager-Controls-Next HH-Pager-Control" data-qa="pager-next" data-page="1" rel="nofollow" href="/search/vacancy?L_is_autosearch=false&amp;clusters=true&amp;enable_snippets=true&amp;search_field=name&amp;text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&amp;page=1">дальше</a>
            npage=npage+1
            nextpage = None
            nextpage = soup.find('a',{'class':'HH-Pager-Controls-Next'})
            if nextpage:
                print (nextpage['href'])

    return serials

vacancies1=gethh(searchtext,maxpage)
print(len(vacancies1))
print(vacancies1)

def getsj(searchtext,maxpage):
    nextpage = True
    npage=1
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
    serials = []
    while nextpage and npage<=maxpage:
        print ('Страница:',npage)
        params = {}
        #https://russia.superjob.ru/vacancy/search/?keywords=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B5%D1%80&page=1
        main_link = 'https://russia.superjob.ru/vacancy/search/?keywords=' + searchtext + '&showClusters=true&page='+str(npage)

        response = requests.get(main_link,headers=header,params=params)

        if response.ok:
            #print(response.text)
            #soup = bs(response.text,'lxml')
            serials_list = re.findall('<a[^>]*?icMQ[^>]*?(\/vakansii\/[^>\/"]*?\-\d+\.html)[^>]*>(.+?)<\/a>.*?<span[^>]*company-item-salary[^>]*>(.*?)<\/span>\s*?<\/div>',response.text)

            if serials_list:
                for serial in serials_list:
                    serial_data = {}
                    #print(serial)
                    serial_data['compensation'] = None
                    serial_data['host'] = 'superjob.ru'
                    serial_data['link'] = 'https://russia.superjob.ru'+ serial[0]
                    serial_data['name'] = re.sub('<[^>]+?>', '', serial[1])
                    serial_data['compensation'] = re.sub('<[^>]+?>', '', serial[2].replace('\xa0',''))


                    serial_data['minsalary'] = None
                    serial_data['maxsalary'] = None
                    serial_data['currency'] = None

                    salary = {}
                    salary=re.search("^(\d+)\s*(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[2],' max:',salary[1])
                        serial_data['currency'] = salary[2]
                        serial_data['minsalary'] = salary[1]
                        serial_data['maxsalary'] = salary[1]
                    salary=re.search("(\d+)\s*\—\s*(\d+)\s*(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[3],' min:',salary[1],'max:',salary[2])
                        serial_data['currency'] = salary[3]
                        serial_data['minsalary'] = salary[1]
                        serial_data['maxsalary'] = salary[2]

                    salary=re.search("от\s*(\d+)\s*(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[2],' min:',salary[1])
                        serial_data['currency'] = salary[2]
                        serial_data['minsalary'] = salary[1]

                    salary=re.search("до\s*(\d+)\s*(\D+)", serial_data['compensation'])
                    if salary:
                        #print('val:',salary[2],' max:',salary[1])
                        serial_data['currency'] = salary[2]
                        serial_data['maxsalary'] = salary[1]


                    print(serial_data)
                    serials.append(serial_data)
            #pprint(serials)

            #<a class="bloko-button HH-Pager-Controls-Next HH-Pager-Control" data-qa="pager-next" data-page="1" rel="nofollow" href="/search/vacancy?L_is_autosearch=false&amp;clusters=true&amp;enable_snippets=true&amp;search_field=name&amp;text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&amp;page=1">дальше</a>
            npage=npage+1
            nextpage = None
            #<a rel="next" class="icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe" target="_self" href="/vacancy/search/?keywords=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B5%D1%80&amp;page=2">
            #print('<a[^>]*next[^>]*\/vacancy\/[^>]*amp;page='+str(npage)+'[^>]*>')
            nextpage = re.search('<a[^>]*next[^>]*page='+str(npage)+'[^>]*>', response.text)
            if nextpage:
                print (nextpage[0])

    return serials

vacancies2=getsj(searchtext,maxpage)
print(len(vacancies2))
print(vacancies2)

vacancies=vacancies1+vacancies2
print(len(vacancies))
#print (vacancies)
df=pd.DataFrame(vacancies)
print(df)

#не обрабатывал ошибки - лень
#по итогам - регуляки всё-таки гибче чем кусок мыла )
