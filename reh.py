import pandas as pd
from fake_useragent import UserAgent
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import re

api_id = 15122868
api_hash = 'xxxx'
string_session = str("xxxx")

ua = UserAgent()

temp = pd.read_csv('db.csv', index_col=0)
pdate = pd.Timestamp("today").strftime("%Y-%m-%d")


def get_soup(url):
    headers = {'User-Agent': ua.random}
    req = Request(url, headers=headers)
    req_url = urlopen(req, timeout=10)
    code = req_url.getcode()

    if code == 200:
        html = req_url.read()
        soup = BeautifulSoup(html, "lxml")
    else:
        soup = ''

    return soup, code


def firstclasshousing():
    url = 'https://www.firstclasshousing.nl/properties?city=Amsterdam&surface=&bedrooms=&max_price=2000'
    df = []
    soup, answer = get_soup(url)
    for i in soup.find_all(class_="grey-border"):
        link = 'https://www.firstclasshousing.nl'+i.get('href')
        text = i.p.text
        price = int(re.findall(r'\d+', str(i.find_all(class_ = 'price')[0]).replace(',',''))[0])
        if 'Leased' not in text and price <= 2500:
            df.append([link, price, pdate])
    return pd.DataFrame(df, columns=['link','price','pdate'])


def engelvoelkers():
    url = 'https://www.engelvoelkers.com/en/search/?q=&startIndex=0&businessArea=residential&sortOrder=DESC&sortField=newestProfileCreationTimestamp&pageSize=18&facets=bsnssr%3Aresidential%3Bcntry%3Anetherlands%3Bdstrct%3Aamsterdam%3Brgn%3Anoord_holland%3Btyp%3Arent%3B'
    df = []
    soup, answer = get_soup(url)
    for i in soup.find_all(class_="ev-property-container"):
        try:
            link = i['href']
            text = i.find_all(class_='ev-teaser-title')[0].text
            price = int(re.findall(r'\d+', str(i.find_all(class_ = 'ev-value')[0]).replace('&nbsp;','').replace('.',''))[0])
            if 'Rented' not in text and price <= 2500:
                df.append([link, price, pdate])
        except:
            pass
    return pd.DataFrame(df, columns=['link','price','pdate'])

def hausing():
    url = 'https://www.hausing.com/properties-for-rent-amsterdam'
    df = []
    soup, answer = get_soup(url)
    for i in soup.find_all(class_="link-post move-up-on-hover w-inline-block"):
        link = 'https://www.hausing.com' + i['href']
        price = int(i.find_all(class_='text-small-5')[1].text)
        if price <= 2500:
            df.append([link, price, pdate])

    return pd.DataFrame(df, columns=['link','price','pdate'])

def expatrentalsholland():
    url = 'https://www.expatrentalsholland.com/offer/in/amsterdam/sort/newest'
    df = []
    soup, answer = get_soup(url)

    for i in soup.find_all(class_="pandlist-container nieuw"):
        link = i.find_all(class_="textlink-design orange")[0]['href']
        price = int(re.findall(r'\d+', str(i.find_all(class_="pand-price")[0].text).replace('.',''))[0])
        #print(link, price)
        if price <= 2500:
            df.append([link, price, pdate])
    return pd.DataFrame(df, columns=['link','price','pdate'])

def denieuweverhuurmakelaar():
    df = []
    for j in range(1,4):
        try:
            url = 'https://denieuweverhuurmakelaar.nl/en/for-rent/?dps_paged='+str(j)
            soup = get_soup(url)[0]

            for i in soup.find_all(class_="listing-item"):
                link = i.find_all(class_='title')[0]['href']
                title = i.find_all(class_='title')[0].text
                price = int(re.findall(r'\d+', str(i.find_all(class_='excerpt')[0]).replace(',',''))[0])

                if 'RENTED OUT' not in title and price <= 2500:
                    #print(link, title)
                    df.append([link, 0, pdate])
        except:
            pass

        return pd.DataFrame(df, columns=['link','price','pdate'])

def jlgrealestate():
    df = []
    url = 'https://jlgrealestate.com/woningen/?lang=en#q1bKScxLV7JSSs1T0lHKKC0tyk_Lzs8vAIqAOFCxgqLMrGIlq2ql3MQKoIyRqYGBUm0tAA'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="card card--wonen card--has-image card--has-overlay card--has-content"):
        try:
            link = i.find_all(class_='card__overlay u-z3')[0]['href']
            price = int(re.findall(r'\d+', str(i.find_all(class_='card__price prose median clean tiny color-gray-100')[0].text).replace('.',''))[0])
            type_ = i.find_all(class_='card__type card__tag back-white')[0].text
            if type_ == 'for rent' and price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def outamsterdam():
    df = []
    url = 'https://out-amsterdam.nl/?advanced_area&advanced_city=amsterdam&slaapkamers&minimum-m2&opleveringsniveau&price_low=0&price_max=2460&submit=Zoeken&wpestate_regular_search_nonce=b472e2a8c1&_wp_http_referer=%2F'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="property_listing property_card_default"):
        try:
            link = i['data-link']
            price = int(re.findall(r'\d+', str(i.find_all(class_='listing_unit_price_wrapper')).replace('.',''))[0])
            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def housingagency():
    df = []
    url = 'https://www.housingagency.nl/for-rent?city=Amsterdam&min_price=&max_price=2000&surface=&bedrooms=&interior='
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="listing regular"):
        try:
            link = 'https://www.housingagency.nl' + i.find_all(class_='grey-border')[0]['href']
            state = i.find_all(class_='label')[0].text
            price = int(re.findall(r'\d+', str(i.find_all(class_='price')[0].text).replace(',',''))[0])
            if price <= 2500 and state != 'Leased':
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def therentalagencyamsterdam():
    df = []
    url = 'https://therentalagencyamsterdam.nl/residential-listings/rent/amsterdam?locationofinterest=Amsterdam&moveunavailablelistingstothebottom=true&orderby=3&orderdescending=true&pricerange.maxprice=2000'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="col-xs-12 col-md-6 objectcontainer"):
        try:
            link = 'https://therentalagencyamsterdam.nl' + i.find_all(class_="sys-property-link")[0]['href']
            try:
                state = i.find_all(class_="object_status")[0].text
            except:
                state = 'ok'

            price = int(re.findall(r'\d+', str(i.find_all(class_="obj_price")[0]).replace(',',''))[0])
            if price <= 2500 and state != 'Under offer':
                df.append([link, price, pdate])
        except:
            pass
    return pd.DataFrame(df, columns=['link','price','pdate'])

def makelaarsinamsterdam():
    df = []
    url = 'https://www.makelaars-in-amsterdam.nl/aanbod/huur/woningen/amsterdam/'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="metalist__item metalist__item--list metalist__item--forrent"):
        try:
            link = 'https://www.makelaars-in-amsterdam.nl' + i.find_all(class_="object__address object__address--metalist")[0].find_all('a')[0]['href']
            price = int(re.findall(r'\d+', str(i.find_all(itemprop="price")))[0])
            state = i.find_all(class_="object__ribbon object__ribbon--forrent object__ribbon--metalist")[0].find_all('span')[0].text

            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def rentastone():
    df = []
    url = 'https://rentastone.nl/?action=epl_search&post_type=rental&property_location=444&property_price_to=2000&sortby=new'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="search-result"):
        try:
            link = i.find_all(class_="search-result-title")[0].find_all('a')[0]['href']
            price = int(re.findall(r'\d+', str(i.find_all(class_="page-price")[0].text).replace('.',''))[0])

            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

        return pd.DataFrame(df, columns=['link','price','pdate'])

def oeihousing():
    df = []
    url = 'https://oeihousing.com'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="col-md-6 col-sm-6 col-xs-12 pt-cv-content-item pt-cv-1-col"):
        try:
            link = i.find_all(class_="pt-cv-animation-left pt-cv-title")[0].find_all('a')[0]['href']
            price = int(re.findall(r'\d+', str(i.find_all(class_="pt-cv-animation-left pt-cv-title")[0].find_all('a')[0].text.replace('.','')))[0])
            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def expatrentals():
    df = []
    url = 'https://expatrentals.com/residential-listings/rent/amsterdam?locationofinterest=Amsterdam&pricerange.maxprice=2000'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="object thumbnail new_forrent"):
        try:
            link = 'https://expatrentals.com'+i.find_all(class_="sys-property-link")[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="obj_price")[0].text.replace(',',''))[0])
            state = i.find_all(class_="object_status new_forrent")[0].text
            if price <= 2500 and state == 'New for rent':
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def woonoplossingen():
    df = []

    url = 'https://www.woonoplossingen.nl/properties/?filter-property-type=18&filter-location=70&filter-status=19'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="property-box property-box-grid property-box-wrapper"):
        try:
            link = i.find_all(class_="entry-title")[0].find_all('a')[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="property-box-price text-theme")[0].text.replace('.',''))[0])
            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def wonen():
    df = []

    url = 'https://www.123wonen.nl/huurwoningen/in/amsterdam'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="pandlist-container nieuw"):
        try:
            link = i.find_all(class_="textlink-design orange")[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="pand-price")[0].text.replace('.',''))[0])
            state = i.find_all(class_="pand-status nieuw")[0].text
            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def hbhousing():
    df = []

    url = 'https://www.hbhousing.nl/aanbod/huur/?adres=&plaats=Amsterdam&prijs=1750&aantal-kamers=&bouwjaar=&oppervlakte=&woonhuisType=&uitgebreid=beschikbaar'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="woning AVAILABLE"):
        try:
            link = i.find_all('a')[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="property-meta-price")[0].text.replace('.',''))[0])
            if price <= 2500:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def rotsvast():
    df = []

    url = 'https://www.rotsvast.nl/woningaanbod/?type=2&query=Amsterdam&city=&street=&distance=0&minimumBedrooms=-1&minimumPrice%5B1%5D=-1&maximumPrice%5B1%5D=-1&minimumPrice%5B2%5D=-1&maximumPrice%5B2%5D=2000&offices%5B1%5D=0&offices%5B2%5D=0'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="residence-gallery clickable-parent col-md-4"):
        try:
            link = i.find_all(class_='clickable-block')[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="residence-price")[0].text.replace('.',''))[0])
            if price <= 2500 and price > 1300:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def terhaarmakelaars():
    df = []

    url = 'https://terhaarmakelaars.nl/en/aanbod/#q1bKL0pJLUqqVLJSSkksKc3NzCvLTy2ySixOVtJRKqksSA3Ozy8qAcpmlJYWKdUCAA'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="woning"):
        try:
            link = i.find_all('a')[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="price")[0].text.replace('.',''))[0])
            if price <= 2500 and price > 1300:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def smitenheinen():
    df = []

    url = 'https://www.smitenheinen.nl/woningaanbod/huur?street_postcode_city=Amsterdam&status=BESCHIKBAAR&rent_price_from=1000&rent_price_till=2000&construction_year_from=&construction_year_till=&living_area_from=&living_area_till=#objects'
    soup = get_soup(url)[0]

    for i in soup.find_all(class_="relative shadow-card bg-white h-full"):
        try:
            link = 'https://www.smitenheinen.nl'+i.find_all(class_='relative block w-full h-full')[0]['href']
            price = int(re.findall(r'\d+', i.find_all(class_="order-2")[0].text.replace('.',''))[0])
            if price <= 2500 and price > 1300:
                df.append([link, price, pdate])
        except:
            pass

    return pd.DataFrame(df, columns=['link','price','pdate'])

def execute(temp):
    new_temp = pd.concat([engelvoelkers(), hausing(), expatrentalsholland()
                          , denieuweverhuurmakelaar(), housingagency(), therentalagencyamsterdam()
                          , oeihousing(), expatrentals(), wonen(), hbhousing()
                          , rotsvast(), terhaarmakelaars(), smitenheinen()])

    new_temp = new_temp[new_temp.link.isin(temp.link.unique()) == False]
    new_temp.reset_index(inplace=True, drop = True)
    temp = pd.concat([temp,new_temp])
    temp.reset_index(inplace=True, drop = True)
    temp.to_csv('db.csv')
    return new_temp

db = execute(temp)

with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
    for i in db.index:

        pdate = db[db.index == i].pdate[i]
        link = db[db.index == i].link[i]
        price = db[db.index == i].price[i]


        message = '**!!NEW PROPERTY!!**'
        message += '\n\n**Дата:** ' + str(pdate)
        message += '\n**Цена:** ' + str(price)
        message += '\n\n**Ссылка:** ' + str(link)

        print(message)

        client.send_message(channel_id, message)
    client.run_until_disconnected()



