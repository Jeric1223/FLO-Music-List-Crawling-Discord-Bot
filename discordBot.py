import discord
from discord.ext import commands
import json

from youtube import createYoutubePlayList, searchYoutubeSong, insertPlayListSong

import requests
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
from io import BytesIO
import os
import time
import sys
import io
import json
import time
from selenium import webdriver

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


token = 'MTA2MDkwNDI4NTM1OTA0NjY5Ng.GNdHYR.xHw2rI_tFXsknIPr-omK88cJd7EWCil28M61YQ'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    
def startPlayList(URL):
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(URL)
    driver.implicitly_wait(time_to_wait=5)
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    prodList = soup.find_all("strong", {"class": "tit__text"})
    title = soup.select('#main > div > div.playlist-badge > div.playlist-badge--left > div.playlist-badge__info > p')
    
    playList = ['',[]]
    playList[0] = title[0].text
    for value in prodList:
        playList[1].append(value.text)

    return playList


@bot.event
async def on_ready():
    print('Bot: {}'.format(bot.user))

@bot.command()
async def 플로리스트출력(ctx):
    flowSongListLink = ctx.message.content.split(' ')[1]
    songUrlList = []

    await ctx.send('리스트를 불러오는중...')
    playListData = startPlayList(flowSongListLink)

    await ctx.send('음악 리스트 유튜브에서 찾는중...')
    for songName in playListData[1]:
        songUrlList.append(searchYoutubeSongCrawing(songName)) 
    
    await ctx.send(songUrlList)
    
    await ctx.send(f'!!재생목록 생성 {playListData[0]}')
    await ctx.send(f'!!재생목록 추가 {playListData[0]} {" | ".join(songUrlList)}')

    

@bot.command()
async def 유튜브리스트생성(ctx):
    try:
        flowSongListLink = ctx.message.content.split(' ')[1]
        
        await ctx.send('리스트를 불러오는중...')
        playListData = startPlayList(flowSongListLink)
        await ctx.send(playListData)
        
        await ctx.send('유튜브 플레이리스트 생성중...')
        youtubePlayListId = createYoutubePlayList(playListData[0])

        videoIdList = []
        await ctx.send(f'유튜브 플레이리스트에 노래 추가하는중... 오래걸릴 수도 있습니다')
        for value in playListData[1]:
            await videoIdList.append(searchYoutubeSong(value))

        await ctx.send(videoIdList)
        for videoId in videoIdList:
            await insertPlayListSong(youtubePlayListId, videoId) 
        
        await ctx.send(f'유튜브 플레이리스트 생성 완료 링크 : https://www.youtube.com/playlist?list={youtubePlayListId}')
    except Exception as e:
        embed=discord.Embed(title="오류!", description=e, color=0xff0000)
        await ctx.send(embed=embed)

   
bot.run(token)