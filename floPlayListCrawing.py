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


driver = webdriver.Chrome(executable_path='chromedriver')
driver.get('https://www.music-flo.com/detail/openplaylist/azonoohdaededoeh')
driver.implicitly_wait(time_to_wait=5)
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, features="html.parser")
prodList = soup.find_all("strong", {"class": "tit__text"})
title = soup.select('#main > div > div.playlist-badge > div.playlist-badge__info > div.playlist-badge__title')

#main > div > div.playlist-badge > div.playlist-badge__info > div.playlist-badge__title

playList = ['',[]]
print(title)
playList[0] = title[0].text
for value in prodList:
    playList[1].append(value.text)

