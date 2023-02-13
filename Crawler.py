from random import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from datetime import datetime as dt
import pandas as pd
import numpy as np
import time
import os
from tqdm.notebook import tqdm

class Crawler:
    def __init__(self):
        # 사이트 선택받은 변수
        self.keyword = None
        
        # user-agent 설정, 쉽게 생각하면 사람이라고 인식하게 만듬
        self.options = Options()
        ua = UserAgent(verify_ssl=False)
        userAgent = ua.random
        self.options.add_argument('headless')
        self.options.add_argument(f'user-agent={userAgent}')
        
        # 크롤링 사이트 선택
    def crawlingSite(self):
        site_kor = {
                    '멜론' : 'https://www.melon.com/chart/day/index.htm',
                    '벅스' : 'https://music.bugs.co.kr/chart/track/day/total',
                    '지니' : 'https://www.genie.co.kr/chart/top200',
                    '플로' : 'https://www.music-flo.com/browse',
                    '바이브' : 'https://vibe.naver.com/chart/total',
                   }
        site_eng = {
                    'Melon' : 'https://www.melon.com/chart/day/index.htm',
                    'Bugs' : 'https://music.bugs.co.kr/chart/track/day/total',
                    'Genie' : 'https://www.genie.co.kr/chart/top200',
                    'Flo' : 'https://www.music-flo.com/browse',
                    'Vibe' : 'https://vibe.naver.com/chart/total',
                    }
        
        if self.keyword in site_kor:
            pass
        elif self.keyword in site_eng:
            pass
        else:
            raise Exception('해당 키워드는 없습니다.')
            
        List = {}
        # 해당 사이트의 주소를 리턴함
        if self.keyword.encode().isalpha():
            if self.keyword == 'Melon':
                List = self.searchMelon(site_eng[self.keyword])
                return List
            elif self.keyword == 'Bugs':
                List = self.searchBugs(site_eng[self.keyword])
                return List
            elif self.keyword == 'Genie':
                List = self.searchGenie(site_eng[self.keyword])
                return List
            elif self.keyword == 'Flo':
                List = self.searchFlo(site_eng[self.keyword])
                return List
            elif self.keyword == 'Vibe':
                List = self.searchVive(site_eng[self.keyword])
                return List    
        else:
            if self.keyword == '멜론':
                List = self.searchMelon(site_kor[self.keyword])
                return List
            elif self.keyword == '벅스':
                List = self.searchBugs(site_kor[self.keyword])
                return List
            elif self.keyword == '지니':
                List = self.searchGenie(site_kor[self.keyword])
                return List
            elif self.keyword == '플로':
                List = self.searchFlo(site_kor[self.keyword])
                return List
            elif self.keyword == '바이브':
                List = self.searchVive(site_kor[self.keyword])
                return List
    
    def writeFile(self, List):
        now = dt.now()
        day = now.strftime('%Y%m%d')
        
        title = []; singer = []; genre = []
        for value in List.values():
            title.append(value[0])
            singer.append(value[1])
            genre.append(value[2])
        
        df = pd.DataFrame(data=(zip(range(1, 101), title, singer, genre)), columns=['순위', '제목', '가수', '장르'])
        
        if os.path.isdir('./songList'):
            pass
        else:
            os.mkdir('./songList')
            
        df.to_csv('./songList/' + self.keyword + "_" + day +'.csv', index=False, encoding = 'utf-8-sig')
        
    def findGenre(self, songList):
        # 각 사이트 별로 크롤링한 Top100 차트를 가지고 장르를 찾아야 하는 함수
        # {1 : [라일락, 아이유], 2 : [롤린, 브레이브걸스] } 이런식으로 데이터가 들어가있음
        tmpList = {}
        for key, value in tqdm(songList.items()):
            try:
                # 네이버에서 먼저 찾음
                self.driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="+value[1]+'+'+value[0]+'+'+"곡정보")
                
                title = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[1]/div[1]/h2/span/strong").text.replace(".", "")
                artist = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[2]/div[1]/div/div[2]/dl/div[1]/dd/a").text
                genre = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[2]/div[1]/div/div[2]/dl/div[4]/dd").text
                
                value = [title, artist, genre]
                tmpList[key] = value
                
                time.sleep(0.5)# 서버에 과부하를 안주기 위해 시간 걸어놓음
            except NoSuchElementException:
                try:
                    try:
                        #지니로 슝
                        self.driver.get('https://www.genie.co.kr/chart/top200')
                        self.driver.find_element_by_xpath('//*[@id="sc-fd"]').send_keys(value[0] + " " + value[1])
                        element = self.driver.find_element_by_xpath('//*[@id="frmGNB"]/fieldset/input[3]')
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.5)
                        
                        try:
                            element = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr/td[4]/a')
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(0.5)
                        except:
                            element = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div[2]/div/table/tbody/tr/td[4]/a')
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(0.5)
                            
                        title = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/h2').text.strip().replace(".", "")
                        artist = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[1]/span[2]/a').text
                        genre = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[3]/span[2]').text
                        
                        value = [title, artist, genre]
                        tmpList[key] = value
                    except:
                        #지니로 슝2
                        self.driver.get('https://www.genie.co.kr/chart/top200')
                        self.driver.find_element_by_xpath('//*[@id="sc-fd"]').send_keys(value[0])
                        element = self.driver.find_element_by_xpath('//*[@id="frmGNB"]/fieldset/input[3]')
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.5)
                        
                        try:
                            element = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr/td[4]/a')
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(0.5)
                        except:
                            element = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div[2]/div/table/tbody/tr/td[4]/a')
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(0.5)
                            
                        title = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/h2').text.strip().replace(".", "")
                        artist = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[1]/span[2]/a').text
                        genre = self.driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[3]/span[2]').text
                        
                        value = [title, artist, genre]
                        tmpList[key] = value
                        
                except NoSuchElementException:
                    try:
                        # 한여름밤의 꿈'이렇게 찾게 변경
                        tmp = value[0].split('(', 1)[0].rstrip()
                        # 다시 네이버에서 찾음
                        self.driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="+value[1]+'+'+ tmp +'+'+"곡정보")
                        time.sleep(0.5)
                        
                        title = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[1]/div[1]/h2/span/strong").text.replace(".", "")
                        artist = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[2]/div[1]/div/div[2]/dl/div[1]/dd/a").text
                        genre = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[2]/div[1]/div/div[2]/dl/div[4]/dd").text
                    
                        value = [title, artist, genre]
                        tmpList[key] = value
    
                        time.sleep(0.5) # 서버에 과부하를 안주기 위해 시간 걸어놓음
                    except:
                        # 한여름밤의 꿈'이렇게 찾게 변경
                        tmp = value[0].split('(', 1)[0].rstrip()
                        # 다시 네이버에서 찾음
                        self.driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="+value[0]+'+'+"곡정보")
                        time.sleep(0.5)
                        
                        title = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[1]/div[1]/h2/span/strong").text.replace(".", "")
                        artist = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[2]/div[1]/div/div[2]/dl/div[1]/dd/a").text
                        genre = self.driver.find_element_by_xpath("//*[@id='main_pack']/div[2]/div[2]/div[1]/div/div[2]/dl/div[4]/dd").text
                    
                        value = [title, artist, genre]
                        tmpList[key] = value
    
                        time.sleep(0.5) # 서버에 과부하를 안주기 위해 시간 걸어놓음
                    
            print(key, value)
            
        return tmpList
    
    def searchMelon(self, url):
        # 셀레니엄 시작
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=ChromeDriverManager().install())
        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.find_all("div", {"class": "ellipsis rank01"}) 
        singers = soup.find_all("div", {"class": "ellipsis rank02"}) 
    
        melonList = {}
        rank = 1
        for t, s in zip(titles, singers):
            melonList[rank] = [t.find('a').text, s.find('span', {"class": "checkEllipsis"}).text]   
            rank += 1

        return melonList 
    
    def searchBugs(self, url):
        # 벅스 일간 Top100 크롤링
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=ChromeDriverManager().install())
        self.driver.get(url)
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        songs = soup.select('p.title > a')
        # artists 부분 p.artsit > a 에서 p.artist로
        artists = soup.select('p.artist')
        bugsList = {}
        rank = 1
        for song, artist in zip(songs, artists):
            # \n가수이름\n 형식으로 나와서 replace
            artist = artist.text.replace('\n', "").rstrip()
            
            if artist[:len(artist)//2] == artist[len(artist)//2:]:
                bugsList[rank] = [song.text, artist[:len(artist)//2]]
            else:
                bugsList[rank] = [song.text, artist]
            
            rank += 1
        return bugsList
    
    def searchGenie(self, url):
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=ChromeDriverManager().install())
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        self.driver.find_element_by_xpath("//*[@id='body-content']/div[3]/ul/li[2]/a").click()
        
        genieList = {}
        rank = 1
        for i in range(1,51): 
            title = self.driver.find_element_by_xpath(f"//*[@id='body-content']/div[4]/div/table/tbody/tr["+str(i)+"]/td[5]/a[1]")
            singer = self.driver.find_element_by_xpath(f"//*[@id='body-content']/div[4]/div/table/tbody/tr["+str(i)+"]/td[5]/a[2]")
            genieList[i] = [title.text, singer.text]

        # 51~100위까지 변경
        time.sleep(2)
        self.driver.find_element_by_css_selector('#body-content > div.page-nav.rank-page-nav > a:nth-child(2)').send_keys(Keys.ENTER)
        
        for i in range(1,51):
            title = self.driver.find_element_by_xpath(f"//*[@id='body-content']/div[4]/div/table/tbody/tr["+str(i)+"]/td[5]/a[1]")
            singer = self.driver.find_element_by_xpath(f"//*[@id='body-content']/div[4]/div/table/tbody/tr["+str(i)+"]/td[5]/a[2]")
            genieList[i+50] = [title.text, singer.text]
            
        return genieList
        
    def searchFlo(self, url):
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=ChromeDriverManager().install())
        self.driver.get(url)
        time.sleep(1)
        element = self.driver.find_element_by_css_selector("#browseRank > div.chart_lst > div > button")
        self.driver.execute_script("arguments[0].click();", element)
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        floList = {}
        for i in range(1,101):
            title = self.driver.find_element_by_xpath(f"//*[@id='browseRank']/div[2]/table/tbody/tr["+str(i)+"]/td[4]/div/div[2]/button/p/strong")
            singer = self.driver.find_element_by_xpath(f"//*[@id='browseRank']/div[2]/table/tbody/tr["+str(i)+"]/td[5]/p/span[1]/span/span/a")
            floList[i] = [title.text, singer.text]
            
        return floList
    
    def searchVive(self, url):
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=ChromeDriverManager().install())
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 처음 뜨는 팝업창 없애기
        self.driver.find_element_by_css_selector("#app > div.modal > div > div > a.btn_close").click()
        time.sleep(3)
        
        titles = soup.findAll('span', {'class':'inner_cell'})
        singers = soup.findAll('td', {'class':'artist'})

        viveList = {}
        rank = 1
        for title, singer in zip(titles, singers):
            viveList[rank] = [title.text, singer.text]
            rank += 1
        
        return viveList
    
    def start(self, keyword):
        self.keyword = keyword
        List = self.crawlingSite()
        List = self.findGenre(List)
        self.driver.quit()
        self.writeFile(List)

if __name__ == '__main__':
    crawl = Crawler()
    crawl.start('멜론')
