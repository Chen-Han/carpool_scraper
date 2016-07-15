#!/usr/bin/python
# -*- coding: utf-8 -*-
import regex_util
import unittest
import re 

_phone_re = "(\d{3,4}).{0,2}(\d{3}).?(\d{4})"

def extract_phone_info(txt):
    match_result = re.search(_phone_re,txt)
    if(not match_result):
        return None
    areaCode = match_result.group(1)
    areaCode = areaCode[1::] if (len(areaCode)==4) else areaCode #without country code
    secondGroup = match_result.group(2) # second num group
    thirdGroup = match_result.group(3)
    return areaCode + secondGroup + thirdGroup



class TestPhoneExtractor(unittest.TestCase):
    def helper_test(self,txt,exp_phone_num):
        phone_num = extract_phone_info(txt)
        self.assertEquals(exp_phone_num,phone_num)

    def test_simple(self):
        txt = "416-989-6302"
        self.helper_test(txt,"4169896302")

    def test_country_code(self):
        txt = "1226.707.7421"
        self.helper_test(txt,"2267077421")

    def test_bracket(self):
        txt = "(226)-707-7421"
        self.helper_test(txt,"2267077421")

    def test_nospace(self):
        txt = "4169896302"
        self.helper_test(txt,"4169896302")


if __name__ == '__main__':
    unittest.main()