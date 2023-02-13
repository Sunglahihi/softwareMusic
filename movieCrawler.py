# -*- coding: utf-8 -*-
"""
Created on Sun May 23 22:06:58 2021

@author: Lee
"""
# noinspection PyUnresolvedReferences
import os
# noinspection PyUnresolvedReferences
import subprocess
# noinspection PyUnresolvedReferences
from pytube import Playlist, YouTube 
from moviepy.editor import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# noinspection PyUnresolvedReferences
from selenium.webdriver.support.ui import WebDriverWait
# noinspection PyUnresolvedReferences
from selenium.webdriver.common.keys import Keys
# noinspection PyUnresolvedReferences
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
# noinspection PyUnresolvedReferences
from datetime import datetime as dt
# noinspection PyUnresolvedReferences
import pandas as pd
# noinspection PyUnresolvedReferences
import numpy as np
import time
import os
# noinspection PyUnresolvedReferences
from tqdm.notebook import tqdm

class movieCrawler:
    def __init__(self, keyword):
        # user-agent 설정, 쉽게 생각하면 사람이라고 인식하게 만듬
        self.options = Options()
        ua = UserAgent(verify_ssl=False)
        userAgent = ua.random
        self.options.add_argument('headless')
        self.options.add_argument(f'user-agent={userAgent}')
        self.keyword = keyword
        self.fpath = lambda x: './src/' + x
        
    def youtubeDown(self):
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=ChromeDriverManager().install())
        self.driver.get("https://www.youtube.com/results?search_query="+self.keyword+" mv")
        self.driver.find_element_by_xpath("//*[@id='video-title']/yt-formatted-string").click()
        time.sleep(0.5)

        video_id = self.driver.current_url
        self.driver.quit()
        
        
        yt = YouTube(video_id)
    
        vpath = (
             yt.streams.filter(adaptive=True, res = '720p', file_extension="mp4", only_video=True)
            .order_by("resolution")
            .desc()
            .all()
          ) 
        
        try:
            vpath = vpath[1].download(output_path=self.fpath("video/"), filename = self.keyword ) 
        except:
            vpath = vpath[0].download(output_path=self.fpath("video/"), filename = self.keyword ) 
            
        apath = ( 
            yt.streams.filter(adaptive=True, file_extension="mp4", only_audio=True)
            .order_by("abr")
            .desc()
            .first()
            .download(output_path=self.fpath("audio/"), filename = self.keyword) 
          )
    
        v = VideoFileClip(vpath)
        a = AudioFileClip(apath)
    
        v.audio = a
    
        if os.path.isdir('./src/merge'):
            pass
        else:
            os.mkdir('./src/merge')
    
    
        v.write_videofile(self.fpath("merge/" + vpath.split('/')[-1]))
        
        
if __name__ == '__main__':
    movie = movieCrawler("상상더하기 - MSG워너비 TOP 8 (별루지, 김정수, 강창모, 정기석, 이동휘, 이상이, 박재정, 원슈타인")
    movie.youtubeDown()