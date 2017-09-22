#!/usr/bin/python
# -*- coding: utf-8 -*-

"""analyzes users carpool request"""

import date_extractor
import location_extractor
from location_extractor import TORONTO, WATERLOO
import regex_util
import unittest
from datetime import datetime

def parse_request(txt, reference_date = None):
    if reference_date is None:
        reference_date = datetime.today()
    normalized_txt = regex_util.normalize(txt)
    date = date_extractor.extract_date_info(normalized_txt,reference_date)
    location_info = location_extractor.extract_location_info(normalized_txt)
    if (location_info):
        return RequestInfo(date,location_info[0],location_info[1])
    return None


class RequestInfo: 
    def __init__(self,date,from_location,to_location):
        self.date = date
        self.from_location = from_location
        self.to_location = to_location

"""
Filter:
On [DATE] [Waterloo/Toronto] to [Toronto/Waterloo]
From [DATE] to [DATE] [Waterloo/Toronto] to [Toronto/Waterloo]
On [DATE1], [DATE2] ... [Waterloo/Toronto] to [Toronto/Waterloo]
Remind [Date] [Waterloo/Toronto] to [Toronto/Waterloo]

"""
class TestRequestAnalyzer(unittest.TestCase):
    def helper_test(self,txt,exp_date,exp_from_location,exp_to_location):
        request_info = parse_request(txt,datetime(2016,7,12))
        self.assertEquals(exp_date,request_info.date)
        self.assertEquals(exp_to_location,request_info.to_location)
        self.assertEquals(exp_from_location,request_info.from_location)

    def test_simple_parse_eng(self):
        text = "On 7.15, loo to trt"
        date = datetime(2016,7,15)
        self.helper_test(text,date,WATERLOO,TORONTO)

    def test_simple_parse_ch(self):
        text = "7月16号 从多伦多到滑铁卢"
        date = datetime(2016,7,16)
        self.helper_test(text,date,TORONTO,WATERLOO)

    def test_normalize(self):
        text = "7月16号 从多伦多到滑铁卢"
        normalized = regex_util.normalize(text)
        print(regex_util.normalize(text))
        print(location_extractor.extract_location_info(text))

    
if (__name__ == "__main__"):
    unittest.main()






