
#!/usr/bin/python
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import datetime
import time
import sys
import io
import json

import httplib2
import os
import sys
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def googleAuthRequestReturnYoutubeObject():
  CLIENT_SECRETS_FILE = "client_secret_428027916524-hc2fvfidflk5c91t4b905ov440hvci8m.apps.googleusercontent.com.json"
  MISSING_CLIENT_SECRETS_MESSAGE = """
  WARNING: Please configure OAuth 2.0

  To make this sample run you will need to populate the client_secrets.json file
  found at:

    %s

  with information from the API Console
  https://console.cloud.google.com/

  For more information about the client_secrets.json file format, please visit:
  https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
  """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    CLIENT_SECRETS_FILE))
  YOUTUBE_READ_WRITE_SCOPE = ['https://www.googleapis.com/auth/youtubepartner', 'https://www.googleapis.com/auth/youtube']

  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    message=MISSING_CLIENT_SECRETS_MESSAGE,
    scope=YOUTUBE_READ_WRITE_SCOPE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

  DEVELOPER_KEY = 'AIzaSyC26mXxI26xSs8B6BjR0MaGQif2BX82HV4' #유튜브 API 키 값
  #service build
  return build('youtube', 'v3', http=credentials.authorize(httplib2.Http()))

def createYoutubePlayList(TITLE):
  youtube = googleAuthRequestReturnYoutubeObject()
  # This code creates a new, private playlist in the authorized user's channel.
  playlists_insert_response = youtube.playlists().insert(
    part="snippet,status",
    body=dict(
      snippet=dict(
        title=TITLE,
      )
    )
  ).execute()

  return playlists_insert_response["id"]

async def insertPlayListSong(id, videoId):
  youtube = googleAuthRequestReturnYoutubeObject()
  # This code creates a new, private playlist in the authorized user's channel.
  try:
    playlists_insert_response = await youtube.playlistItems().insert(
      part="snippet",
      body={
        "snippet": {
        "playlistId": id,
        "resourceId": {
          "kind": "youtube#video",
          "videoId": videoId
          }
        }
      }
      ).execute()
  except:
    print('insert 오류')

async def searchYoutubeSong(query):
  youtube = googleAuthRequestReturnYoutubeObject()
  # This code creates a new, private playlist in the authorized user's channel.
  try:
    search_response = await youtube.search().list(
      q=query,
      part="id,snippet",
      maxResults=1
    ).execute()

    return search_response['items'][0]['id']['videoId']
  except:
    return 





