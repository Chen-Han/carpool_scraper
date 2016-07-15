#!/usr/bin/python
# -*- coding: utf-8 -*-
import regex_util
import re

TORONTO = "Toronto"
WATERLOO = "Waterloo"
toronto_re = regex_util.combine_regex_or("toronto","trt","多伦多",
    "多村","north york","ny","northyork","sheppard","yonge","finch","downtown","dt","yorkdale",
    "fairview","fmall","fm","stc","scarborough","pacific","pmall")

waterloo_re = regex_util.combine_regex_or("waterloo","loo","滑铁卢","水卢","卢村","uw","burgerking",
    "burger king","bk","plaza","汉堡王","dc","williams")

def extract_location_info(txt):
    if(not txt):
        return None
    trt_result = re.search(toronto_re,txt)
    loo_result = re.search(waterloo_re,txt)
    if(trt_result and loo_result):
        if(trt_result.end() < loo_result.end()):
            return (TORONTO,WATERLOO) # trt -> loo
        else:
            return (WATERLOO,TORONTO)
    return None

