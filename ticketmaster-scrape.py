#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 04:17:38 2018

@author: ranjit
"""


import os
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from dateutil.parser import parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from collections import OrderedDict
import csv
import traceback
import json

def month_to_num(name):
    if name == "jan": return '01'
    elif name == "feb": return '02'
    elif name == "mar": return '03'
    elif name == "apr": return '04'
    elif name == "may": return '05'
    elif name == "jun": return '06'
    elif name == "jul": return '07'
    elif name == "aug": return '08'
    elif name == "sep": return '09'
    elif name == "oct": return '10'
    elif name == "nov": return '11'
    elif name == "dec": return '12'
    else: raise 'valueerror'

fields= OrderedDict([('ai_id', None),
('category', None),
('event_name', None),
('event_desc', None),
('start_date', None),
('start_time', None),
('end_date', None),
('end_time', None),
('host_name', None),
('location_name', None),
('location_address', None),
('location_desc', None),
('host_contact', None),
('lat', None),
('lng', None),
('image_name', None),
('city', None),
('ticket_link', None),
('facebookhost_id', None),
('website', None),
('facebook_id', None),
('linkedin_id', None),
('twitter_id', None),
('instagram_id', None),
('pinterest_id', None),
('google_id', None),
('skype_id', None),
('youtube_id', None),
('discord_id', None),
('snapchat_id', None),
('ello_id', None),
('periscope_id', None),
('vimeo_id', None),
('meerkat_id', None),
('vine_id', None),
('flickr_id', None),
('tumblr_id', None),
('medium_id', None),
('tripadvisor_id', None),
('dribble_id', None),
('whatsapp_id', None),
('search_value', None),
('parent_event', None),
('marker', None),
('site_scraped', None)])

#tm_client = ticketpy.ApiClient('Nu77RwY7bX8B7PCJyDF30cvIM1SRSSGQ')

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--ignore-certificate-errors')
#chromeOptions.add_argument('--headless') 
#chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(dir_path+'/chromedriver')
driver.implicitly_wait(3)
pageid=1
pageno=1

driver.get("https://www.ticketmaster.no/musikk/alle-musikk/10001/events?countries=578&page="+str(pageno))
maxpage=1
for pageid in range(1,maxpage+1):
    
    csvfile = dir_path+'/ticketmaster/scrape-'+str(pageno)+'.csv'
    #social_link = dir_path+'/social_link.csv'
    header = ['ai_id', 'category', 'event_name', 'event_desc', 'start_date', 'start_time', 'end_date', 'end_time', 'host_name', 'location_name', 'location_address', 'location_desc', 'host_contact', 'lat', 'lng', 'image_name', 'city', 'ticket_link', 'facebookhost_id', 'website', 'facebook_id', 'linkedin_id', 'twitter_id', 'instagram_id', 'pinterest_id', 'google_id', 'skype_id', 'youtube_id', 'discord_id', 'snapchat_id', 'ello_id', 'periscope_id', 'vimeo_id', 'meerkat_id', 'vine_id', 'flickr_id', 'tumblr_id', 'medium_id', 'tripadvisor_id', 'dribble_id', 'whatsapp_id','search_value','parent_event','marker','site_scraped']
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(header)
        
    #driver.get('https://trdevents.no/events/list/?tribe_event_display=list&tribe-bar-date=2018-03-01')
    
    #print(jstr["_links"]["last"]["href"])
    main_window = driver.current_window_handle
    try:
        event_link=driver.find_elements_by_css_selector('#national-events > div > ul')
    except:
        event_link=driver.find_elements_by_css_selector('#national-events > div > ul')
    print(len(event_link))
    eventid=1
    for event in event_link:
        print (eventid)
        print('')
        print('')
        print('')
        #Event Name
        en=event.find_element_by_css_selector('li.table__cell--eventname > div').text
        fields['event_name']=en
        print("Event Name:"+en)
        
        #site_scraped
        fields['site_scraped']=driver.current_url
        print("Site scraped : "+fields['site_scraped'])
        
        #ticket link
        ticket_link=''
        try:
            ticket_link = event.find_element_by_css_selector('li.table__cell--availability > div > a').get_attribute('href')
        except:
            ticket_link = event.find_element_by_css_selector('li.table__cell--availability > div > a.link--viewdates').get_attribute('href')
        fields['ticket_link'] = ticket_link
        print("ticket link : "+fields['ticket_link'])
        
        #location_name
        location_name = ''
        try :
            location_name = event.find_element_by_css_selector('li.table__cell--location > div > h4 > a').text
            fields['location_name'] = location_name
            print(fields['location_name'])
            
        except Exception:
            #print(traceback.format_exc())
            print ('--no location_name')
        #start-date
        start_date=''
        try:
            date=event.find_element_by_css_selector('li.table__cell--date > div > div > span.calendaritem__day').text
            month=event.find_element_by_css_selector('li.table__cell--date > div > div > span.calendaritem__date--month > span.calendaritem__date__item.month').text
            yr=event.find_element_by_css_selector('li.table__cell--date > div > div > span.calendaritem__date--month > span.calendaritem__date__item.year').text
            start_date=date+month_to_num(month)+yr
            fields['start_date']=start_date
            fields['end_date']=start_date
        except:
            print("no date")
        
        #start_time
        try:
            start_time=event.find_element_by_css_selector('li.table__cell--date > div > div > span.calendaritem__date--day > span.calendaritem__date__item.time').text
            #start_times=start_time.split(',')
            #start_time=start_times[1].strip()
            fields['start_time']=start_time
            #print(fields)
            print(start_time)
        except:
            print('no start time')
            
        #city
        #addr=location_name.split(',')
        #city=addr[1].strip()
        try:
            city=event.find_element_by_css_selector('li.table__cell--location > div > div').text
        except:
            print('No city present')
        fields['city']=city
        print(city)
        
        #print(event.get_attribute('innerHTML'))
        try:
            url_value = event.find_element_by_css_selector('li.table__cell--availability > div > a')
        except:
            url_value = event.find_element_by_css_selector('li.table__cell--availability > div > a.link--viewdates')
        print(url_value)
        url_value.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to_window(driver.window_handles[1])
        sleep(1)
        #break
        
        
        try:
            driver.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div.modal__footer > button').click()
        except:
            print("Platinum card request not found")
        sleep(1)    
        try:
            driver.find_element_by_css_selector('#eventinfo > header > div.eventinfo__main__info > div > div.eventcard__body').click()
        except:
            driver.find_element_by_css_selector('body > div.ReactModalPortal > div > div > div > div.modal__footer > button').click()
            sleep(1)
            driver.find_element_by_css_selector('#eventinfo > header > div.eventinfo__main__info > div > div.eventcard__body').click()
            print("handling popup exception")
        sleep(1)
        event_desc = driver.find_element_by_css_selector("body > div.ReactModalPortal > div > div > div > div.special_info_content__container > div.special_info_content__event_info_container > div > div > div").text
        fields['event_desc']= " ".join(event_desc.split())
        print("Event Desc:"+event_desc)
        imgfolder=dir_path+'/ticketmaster/images/scrape-'+str(pageno)#/'+event_name
        if not os.path.exists(imgfolder):
            os.makedirs(imgfolder)
        
        try:
            print("Downloading image for event : "+en)
            img_src=driver.find_element_by_css_selector('#eventinfo > header > img').get_attribute('src')
            print(img_src)                                           
            img_name=img_src[(img_src.rfind('/')+1):]
            urllib.request.urlretrieve(img_src, imgfolder+'/'+img_name)
            fields['image_name']=img_name
            print("Downloaded image for event :"+en)
            
        except Exception:
            print("No image to download")
            print(traceback.format_exc())
        #driver.close()
        #driver.switch_to_window(driver.window_handles[0])
        #driver.switch_to_window(main_window)
        #location_address
        location_address = ''
        try :
            addrurl=event.find_element_by_css_selector('li.table__cell--location > div > h4 > a')
            #url_value.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.get(addrurl.get_attribute('href'))
            driver.switch_to_window(driver.window_handles[1])
            sleep(1)
            addr=driver.find_element_by_css_selector('#infomodule > div > div.infomodule__wrapper > div.infomodule__general > p.infomodule__address').text
            print("rest of address : "+addr)
            location_address = location_name+', '+addr
            fields['location_address'] = location_address
            print(fields['location_address'])
            
        except Exception:
            print(traceback.format_exc())
            print ('--no location_address')
        #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        #driver.switch_to_window(driver.window_handles[1])
        driver.get('https://www.latlong.net/')
        inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
        inputEle.send_keys(addr)
        driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > button').click()
        #latitude
        lat=''
            
        #longitude
        lng=''
        
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                          'Timed out waiting for PA creation ' +
                          'confirmation popup to appear.')
        
            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
            lat=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div > input').get_attribute('value')
            lng=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div:nth-child(2) > input').get_attribute('value')
            print(lat)
            print(lng)
            fields['lat']=lat
            fields['lng']=lng
            pass
        driver.close()
        driver.switch_to_window(main_window)
        with open(csvfile, "a", encoding='utf-8') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(list(fields.values()))
        fields = fields.fromkeys(fields, None)
           
        print('============================================')
        print('')
        eventid=eventid+1
    driver.find_element_by_css_selector('#event-listing > div.pagination--search > ul > li.pagination__lastitem.pagination__item > a').click()
        
        
driver.close()

