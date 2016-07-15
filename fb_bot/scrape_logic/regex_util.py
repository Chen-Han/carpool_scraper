# -*- coding: utf-8 -*-
import array 


def combine_regex_or(*args):
    return "(" + "|".join(args) + ")"

def concat_regex(*args):
    return "(" + "".join(args) + ")"

def name_regex(p,name):
    return "(?P<"+name+">"+p+")"

def normalize(text):
    lowered =  text.lower()
    return make_unicode(lowered)

def make_unicode(text):
    return text.encode('utf-8')