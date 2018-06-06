# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:14:57 2018

@author: yasi
"""
import subprocess # to call jar file inside python
import re
import os
import requests
from bs4 import *
from bs4 import BeautifulSoup
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime, timezone
import pytz
import datetime as dt
import time
from dateutil.tz import gettz
import json
import csv
import json
from pprint import pprint
import gensim, logging
import collections
import codecs
import unicodedata
#from magpie import Magpie
#import pbs

def pretty_json(inFile, out_file):
    obj = None
    with open(inFile, encoding="utf-8", errors="ignore") as f:
        obj = json.load(f)
    #obj = json.loads(obj1.decode("utf-8"))
    outfile = open(out_file, "w")
    outfile.write(json.dumps(obj, indent=4, sort_keys=True))
    outfile.close()


def check_redundancy(fileName):
    read_file=open(fileName, "r", encoding='utf-8',errors='ignore')
    tmpList=[]
    
    for line in read_file:
        words = line.split(",")
        if str(words[0]) in tmpList:
            print(str(words[0]))
        else:
            tmpList.append(str(words[0]))
            

def delSpecificCharsFromFile(fileName,char_list):
    read_file=open(fileName, "r", encoding='utf-8')
    tmpList=[]
    for line in read_file:
        line=line.lower()
        for char in char_list:
            char=char.lower()
            line=line.replace(char," ")
            line=line.replace(u'\xA0', u'')
            line=line.replace(u'\0x92', u'')
            line=line.replace(u'\PU2', u'')
        #line=re.sub(' (co)+ ', ' ', line)
        tmpList.append(line)
    with open(fileName+"deletedSpecificChars.csv", "w",encoding='utf-8') as written_file:
        for val in tmpList:
            written_file.write(val+"\n")
        written_file.close()

def del_extra_lines(fileName):#.csv
    read_file=open(fileName, "r", encoding='utf-8',errors='ignore')
    tmpList=[]
    for line in read_file:
        if len(line)>2:
            line=line.replace("\n","")
            line=line.replace(chr(96),"")
            line=line.replace(chr(39),"")
            line=line.strip()
           # line=line.replace(u'\x92', u'')
            tmpList.append(line)
        
    with open(fileName+"44.csv", "w") as written_file:
        for val in tmpList:
            written_file.write(val+"\n")
        written_file.close()
    
def find_latest(path):
    fname_list=sorted(os.listdir(path))
    fname=fname_list[len(fname_list)-1]
    return fname   
         
        
def remove_charslist_inside_str(string,char_list):
    string=string.lower()
    #line=line.replace("\\", ' ')
    #line.decode("utf-8").replace(u"\U+02BC", "").encode("utf-8")
    #line=line.replace(u'\02BC','')
    char_list=[x.lower() for x in char_list]
    strtmp=""
    strSplits=string.split(" ")
    for char in strSplits:
        if char not in char_list:
           strtmp+=" " 
           strtmp+=char
    
    strtmp=strtmp.replace("  ","") 
    strtmp=strtmp.strip()
#   line=line.replace(char,"")
#    line=line.replace(u'\xA0', u'')
#    line=line.replace(u'\0x92', u'')
#    #line=line.replace(u'\PU2', u'')
#    line=line.replace(u'\8217', u'')
#    line=line.replace(u'\19', u'')
    #print(line.find(u'’'))
    #line=line.encode('ascii', 'ignore')
    return strtmp

#TODO: add option on which encoding is required by user 
def read_file_return_list(fileName):
#    read_file=open(fileName, "r", encoding='ascii' ,errors='ignore') #py 3
    read_file=codecs.open(fileName, encoding='utf-8',errors='ignore', mode='r') #py 2.7
#    read_file=unicodedata.normalize('NFKD', read_file).encode('ascii', 'ignore')

    
    whole_list=[]
    separator=" "
    for line in read_file:
        line=line.lower()
        line=line.replace("\n"," ")
        line=line.replace("\r","")
        line=line.strip()
        whole_list.append(line)
    return whole_list # is a list of lists
    
def remove_charslist_inside_wordslist(wordsList, removeable_items_list , digits=None):#use find
    refined_list=[]
    for word in wordsList:
        if word != u'':
            word=word.strip()
            word=word.replace(u'’s', u'')
            r=10
            if digits==True:
                word = ''.join([i for i in word if not i.isdigit()])
            for item in removeable_items_list:
                word=word.replace(item," ")
            word=word.strip()
            refined_list.append(word)
    return refined_list
    
    
def remove_wordslist_from_wordlist(wordsList, removeable_items_list ):#use in 
    refined_list=[]
    for word in wordsList:
        if len(word)>2:
            if word not in removeable_items_list:
                refined_list.append(word)
    return refined_list

#everything here is based on utf-8
def read_news(news_str=None ,news_file=None, out_file=None): #news.csv
    common_words_list=read_file_return_list("commonWordsV10.txt")# output: a list 
    common_chars_list=read_file_return_list("commonCharsV10.txt")# output: a list

    if(out_file!=None):
#        written_file=open(out_file, "w", encoding='utf-8' ,errors='ignore')#py 3
        written_file=open(out_file, "w")#py 2.7
    
    #mainTextLists=readFromFileReturnListofList(mainTextFileName)# output: a list of lists
    
    return_str=''
    
    if(news_str!=None):
        news_str=news_str.replace("\n"," ")
        news_str=news_str.replace("\t"," ")
        line = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', news_str)
        line=line.lower()
#        line.replace('\u',' ')
        lineWordsList = line.split(" ")
            
        ref_list=remove_charslist_inside_wordslist(lineWordsList,common_chars_list, digits=True)
        ref_list2=remove_wordslist_from_wordlist(ref_list,common_words_list)
        #ref_list2=removeIfInsideWord(refList2,common_chars_list, digits=True)

    elif(news_file!=None):
        #read_file=open(news_file, "r", encoding='utf-8' ,errors='ignore') # py 3
        read_file=open(news_file, "r") #py 2.7
        read_file=read_file.encoding('UTF-8')#py 2.7
       
        for line in read_file:
            line=line.lower()
            line=line.replace("\n","")
            for item in in_paranthesis_words:
                line=line.replace(item,'')
            
            line_words_list = line.split(" ")
            ref_list=remove_charslist_inside_wordslist(line_words_list,common_chars_list, delete_digits=True)
            ref_list2=remove_wordslist_from_wordlist(ref_list,common_words_list)
            #ref_list2=removeIfInsideWord(refList2,common_chars_list, digits=True)
    text=u' '
    for item in ref_list2:
        if (len(item)>1):
            text=text+u' '+item
        text=text.strip()
    # print(abv+","+compName)
    if(out_file!=None):
#        text=text.replace(u'\u2019'," ")
        written_file.write(text)
        written_file.close()
    else:
      return_str=return_str+u' '+text  
      return return_str

        
    

#readNews("sampleNews.txt") 
