#!/usr/bin/python
# -*- coding: utf-8 -date_res*-

from bs4 import BeautifulSoup
import requests
from re import compile
import date_extractor
import location_extractor
import phone_extractor
import datetime
import unittest
import regex_util
from fb_bot.models import Post
import traceback,sys
def parse_to_soup(url):
    return BeautifulSoup(requests.get(url).text,'lxml')

_is_normal_thread_re = compile("normalthread")

def is_normal_thread(tag):
    return tag.name == "tbody" and tag.has_attr('id') and _is_normal_thread_re.match(tag['id'])


_is_post_message_re = compile("postmessage")
def is_post_message(tag):
    return tag.name == "td" and tag.has_attr('id') and _is_post_message_re.match(tag['id'])

# given a post page (beautiful soup obj), extracts the main post content (the first floor)
def getMainPost(post_page):
    main_floor = post_page.find(is_post_message)
    if(not main_floor):
        return None
    return main_floor.text

def scrape_phone_num(post_text):
    if(not post_text):
        return None
    normalized_txt = regex_util.normalize(post_text)
    return phone_extractor.extract_phone_info(normalized_txt)



def scrape_page(carpool_page_url):
    carpool_page = parse_to_soup(carpool_page_url)
    threads =  carpool_page.find_all(is_normal_thread)
    post_list = []
    today = datetime.datetime.today()
    for thread in threads:
        try:
            title = thread.find('span',{'class':'comiis_common'})
            print('Getting thread %s ' % title)
            link = title.find('a',{'onclick':'atarget(this)'})
            normalized_txt = regex_util.normalize(link.text)
            date = date_extractor.extract_date_info(normalized_txt,today)
            location_pair = location_extractor.extract_location_info(normalized_txt)
            
            post_url = link['href']
            post_page = parse_to_soup(post_url) #getting the page
            phone_num = scrape_phone_num(getMainPost(post_page)) # getting the phone number
            # add to list
            if (post_url and date and location_pair):
                post_list.append(Post(carpool_date=date,
                    from_location=location_pair[0],
                    to_location=location_pair[1],
                    phone=phone_num,url=post_url,
                    original_title=link.text,scrape_date=today))
        except Exception as e: 
            print(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            print "*** print_exc:"
            traceback.print_exc()
    return post_list

if __name__ == '__main__':
    _page_to_scrape = 'http://bbs.uwcssa.com/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=54'
    scrape_page(_page_to_scrape)

