#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import calendar
import datetime
import regex_util

def combine_regex_or(*args):
    return regex_util.combine_regex_or(*args)

def concat_regex(*args):
    return regex_util.concat_regex(*args)

def name_regex(p,name):
    return regex_util.name_regex(p,name)


num_re = "(\d{1,2})" # one or two digits
separator_re = "(\.|-|\s+|/)"
eng_month_re = name_regex("((january|jan)|(february|feb)|(march|mar)|(april|apr)|(may)|(june|jun)|(july|jul)|(august|aug)|(september|sept)|(october|oct)|(november|nov)|(december|dec))","en_mon")
eng_month_to_int ={'mar': 3, 'feb': 2, 'aug': 8, 'sep': 9, 'apr': 4, 'jun': 6, 'jul': 7, 'jan': 1, 'may': 5, 'nov': 11, 'dec': 12, 'oct': 10} 
chinese_month_num_re = "(一|二|三|四|五|六|七|八|九|十){1,3}"
chinese_digit_to_int = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}
int_to_chinese_digit = {v:k for k,v in chinese_digit_to_int.items()}
chinese_month_re = concat_regex(name_regex(combine_regex_or(chinese_month_num_re,num_re),"ch_mon"),"\s*月")
month_re = combine_regex_or(chinese_month_re,eng_month_re)

# date of month token
dom_re = concat_regex(name_regex(combine_regex_or(chinese_month_num_re,num_re),"dom"),"(\s*(?P<dom_sfx>(日|号|st|nd|th))?)")

numeric_re = concat_regex(name_regex(num_re,"month"),separator_re, name_regex(num_re,"day"))

# day of week
chinese_dow_re = concat_regex("(周|星期)",name_regex("(一|二|三|四|五|六|1|2|3|4|5|6|(日|天))","ch_dow"))
eng_dow_re = name_regex("((monday|mon)|(tuesday|tue)|(wednesday|wed)|(thursday|thu)|(friday|fri)|(saturday|sat)|(sunday|sun))","en_dow")
end_dow_to_int = {'wed': 2, 'sun': 6, 'fri': 4, 'tue': 1, 'mon': 0, 'thu': 3, 'sat': 5}

def two_digit_num_to_ch(num):

    result = ""
    tens = num/10
    if(tens > 0):
        result = (int_to_chinese_digit[tens] if (tens>1) else "") + int_to_chinese_digit[10]
    digit = num%10
    if(digit > 0):
        result = result + int_to_chinese_digit[digit]
    return result

two_digit_num_map = {two_digit_num_to_ch(n):n for n in range(1,99)}
def ch_to_two_digit_num(ch):
    return two_digit_num_map[ch]


#given a token like "21","十一", parse it to an int
def parse_ch_num_token(token):
    # numeric
    numeric = re.search(num_re,token)
    if(numeric):
        return int(numeric.group(0))
    #chinese month
    ch_mon = re.search(chinese_month_num_re,token)
    if(ch_mon):
        return ch_to_two_digit_num(ch_mon.group(0))
    return None

def parse_en_dow(token):
    abbr = token[0:3]
    return end_dow_to_int[abbr]

def parse_ch_dow(token):
    num = parse_ch_num_token(token) # will parse monday to saturday successfully
    if(num):
        return num - 1 #monday will have value 1, but we want 0
    elif(token == "日" or token == "天"):
        return 6 # must be sunday, 周日
    else:
        return None

def parse_en_mon_token(en_mon): 
    return eng_month_to_int[en_mon[0:3]] #use only the first 3 letter for abbreviation

# ref_date the reference day from when the search starts
# weekday the day of the week to lookfor
def next_weekday(ref_date,weekday):
    days_ahead = weekday - ref_date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return ref_date + datetime.timedelta(days_ahead)
def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


# main function to be used

def extract_date_info(txt,ref_date):
    month,date = extract_date_month(txt)
    if(month and date and month >= 1 and month <= 12 and date<=31):
        year = ref_date.year if(month >= ref_date.month) else ref_date.year + 1
        return datetime.datetime(year,month,date)

    dow = extract_dow(txt) # day of week
    if(dow>=0):
        return roundTime(dt=next_weekday(ref_date,dow),roundTo=60*60*24)
    if(date and date <= 31): #last 五resort
        month = ref_date.month
        year = ref_date.year
        if(date < ref_date.day):
            month = month + 1
            if(month > 12):
                year = year + 1
                month = 1
        return datetime.datetime(year,month,date)
    return None



def extract_date_month(txt):
    month,month_res = extract_month(txt)
    if(month_res):
        # search for date after month
        date_txt = txt[month_res.end():min(len(txt),month_res.end()+9)] # give 9 unicode space window (some chinese characters take upto 3 spaces)
        date = extract_date(date_txt)
        if(date):
            return (month,date)
    # prefer matching txt like 7.2 12-24 for date
    numeric_res = re.search(numeric_re,txt)
    if(numeric_res):
        return (int(numeric_res.group("month")),int(numeric_res.group("day")))
    # fall back to date only if nothing can be found, e.g. 5, 1st, 2nd
    # might not be the actual date
    date = extract_date(txt,more_stringent=True) # search entire txt for date
    return (None,date)




def extract_date(txt,more_stringent=False):
    date_res = re.search(dom_re,txt)
    if(not date_res):
        return None
    if(more_stringent and not date_res.group("dom_sfx")):
        return None
    return parse_ch_num_token(date_res.group("dom"))


def extract_month(txt):
    month_res = re.search(month_re,txt)
    if(month_res):
        en_month_token = month_res.group("en_mon")
        ch_month_token = month_res.group("ch_mon")
        if(ch_month_token):
            return (parse_ch_num_token(ch_month_token),month_res)
        if(en_month_token):
            return (parse_en_mon_token(en_month_token),month_res)
    else:
        return (None,month_res)

def extract_dow(txt):
    ch_dow_res = re.search(chinese_dow_re,txt)
    en_dow_res = re.search(eng_dow_re,txt)
    if(ch_dow_res):
        return parse_ch_dow(ch_dow_res.group("ch_dow"))
    elif(en_dow_res):
        return parse_en_dow(en_dow_res.group("en_dow"))
    else:
        return None

def test_pattern():
    test_txt = "Sunday 7月1号 十月十号 7   10，星期天，提供Waterloo 往返 Toronto or 机场 Carpool".lower()

    search_res = re.search(month_re,test_txt)
    date_txt = test_txt[search_res.end():search_res.end()+9] # give 9 unicode space window (some chinese characters take upto 3 spaces)
    date_res = re.search(dom_re,date_txt)
    ch_dow_res = re.search(chinese_dow_re,test_txt)
    en_dow_res = re.search(eng_dow_re,test_txt)
    en_month_token = search_res.group("en_mon")
    ch_month_token = search_res.group("ch_mon")

    numeric_res = re.search(numeric_re,test_txt)
    if(numeric_res):
        print (int(numeric_res.group("month")))
        print (int(numeric_res.group("day")))

    print (parse_ch_num_token(ch_month_token))
    print (parse_ch_num_token(date_res.group("dom")))
    print (parse_en_dow(en_dow_res.group("en_dow")) if (en_dow_res) else None)
    print (parse_ch_dow(ch_dow_res.group("ch_dow")) if (ch_dow_res) else None)

def test_integration():
    test_txt = " 【7座车+免费WIFI】6/27 28 30, 7/4 6 11机场往返欢迎拼车".lower()
    print(extract_date_info(test_txt,datetime.datetime(2016,11,23)))

if(__name__ == "__main__"):
    test_integration()


