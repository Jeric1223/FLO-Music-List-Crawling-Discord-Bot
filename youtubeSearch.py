# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
from selenium import webdriver
from io import BytesIO
import os
import time
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def searchYoutubeSongCrawing(songName):
    BASE_URL = 'https://www.youtube.com'
    url = f'https://www.youtube.com/results?search_query={songName}'
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url)
    driver.implicitly_wait(time_to_wait=5)
    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    songNameData = soup.select('a#video-title')

    return BASE_URL + songNameData[0]['href']
    

