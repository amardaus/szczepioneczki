from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sched
from playsound import playsound
from babel.dates import format_datetime
import datetime as dt
import unidecode

website = 'https://szczepienia.github.io/'
province = 'malopolskie'
url = website + province
seconds = 2
maxtime = 7 # days

# jeszcze zrobic mozliwosc wyboru miasta, rodzaju szczepionki itp

def findVaccine():
    driver = webdriver.Chrome('./chromedriverx')
    driver.get(url)
    time.sleep(1)
    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser');
    nexttime_element = soup.find('time', {'id': 'nexttime'})
    if nexttime_element.has_attr('datetime'):
        nexttime = nexttime_element['datetime']
    currenttime = datetime.now()
    # print(currenttime.hour)
    # print(nexttime) # convert to datetime

    rows = soup.find('table', {'id': 'szczepienia'}).find('tbody').find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        vcity = cols[0].text
        vtype = cols[3].text
        
        vremove = cols[1].findAll('small')
        for vr in vremove:
            vr.decompose()
        vdate = cols[1].text
        
        
        #print(format_datetime(dt.datetime.today(), locale='pl_PL'))
        months = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"]
        
        vdatenum = unidecode.unidecode(vdate).replace(" ", "")
        #vdatenum = ascii(vdatenum)
        i = 1
        for month in months:
            #vdatenum = vdate.replace(month, "." + str(i))
            if(i < 10):
                vdatenum = vdatenum.replace(month, ".0" + str(i))
            else:
                vdatenum = vdatenum.replace(month, "." + str(i))
            i = i+1
        
        vdatenum = vdatenum + ".2021"
        vdatenum = ascii(vdatenum)
        vdatetime = datetime.strptime(vdatenum, '\'%d.%m.%Y\'');
        now = datetime.now()
        days = (vdatetime-now).days
        
        if days < days:
            if vtype == 'Pfizer' and vcity == 'Kraków':
                print('Znaleziono szczepienie \t [' + vcity + ', ' + vdate + ']')
                #playsound('alert.mp3')

    driver.quit()


s = sched.scheduler(time.time, time.sleep)
def checkTime(sc): 
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    times = soup.find_all('time', class_='timeago')
    lasttime = times[0].text
    nexttime = times[1].text
    lt = datetime.strptime(lasttime, '%Y-%m-%d %H:%M')
    nt = datetime.strptime(nexttime, '%Y-%m-%d %H:%M')
    now = datetime.now()
    

    diff = (now-lt).seconds
    #if diff < 60:
    #    findVaccine()
    findVaccine()
    
    s.enter(seconds, 1, checkTime, (sc,))
    #print(str(lt.hour) + ":" + str(lt.minute))
    #print(str(nt.hour) + ":" + str(nt.minute))
    #print(str(now.hour) + ":" + str(now.minute))

s.enter(seconds, 1, checkTime, (s,))
s.run()
