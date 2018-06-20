import requests
from bs4 import BeautifulSoup
from queue import Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import os
from turkish import capitalize
from datetime import datetime


q=Queue()
reg={}
songs=[]
file = open("C:/Users/asus/youtube-mp3-log.txt","a")

def pulldata(query):
    video_links = []
    video_titles=[]
    url = "https://www.youtube.com/results?search_query="

    url=url+query
    r=requests.get(url)
    source_code = r.content
    soup = BeautifulSoup(source_code, "html.parser")
    links = soup.find_all("a")

    for link in links:
        title=link.get("title")
        video_id=link.get("href")
        video_titles.append(title)


        if "watch?v=" in video_id:
            video_links.append(video_id)

    keys = query.split()
    for t in video_titles:
        if capitalize(keys[0]) in str(t):
            index = (video_titles.index(t))
            break

    reg[video_links[0]] = video_titles[index]





    q.put("https://www.youtube.com"+video_links[0])
    reg[video_links[0]]=video_titles[index]
    file.write(video_titles[index] + "======" + datetime.now().strftime("%c") + "\n")





def exists(path):
    try:
        st = os.stat(path)

    except os.error:
        return False

    return True

opt = Options()
opt.add_argument("--disable-notifications")

n_of_songs = int(input("Kaç şarkı indirmek istiyorsunuz?"))
for i in range(n_of_songs):
    name = input("Şarkı-{}:".format(i+1))
    songs.append(name)

print("İndirme başlatılacak. Lütfen bekleyin...")
for song in songs:
    pulldata(song)


driver = webdriver.Chrome(chrome_options=opt, executable_path="C:\chromedriver.exe")

for get in range(len(songs)):
    driver.get("https://www.onlinevideoconverter.com/mp3-converter")
    element = driver.find_element_by_name("texturl")
    element.send_keys(q.get(), Keys.ENTER)


    try:
        window_before = driver.window_handles[0]
        downloadElem=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID,"downloadq")))
        downloadElem.click()
        driver.switch_to.window(window_before)

    except TimeoutException:
        print("Timeout Error or Copyright issues!")






last_item = list(reg.values())[len(reg)-1]
while True:
    time.sleep(0.5)
    if exists("C:/Users/asus/Downloads/"+last_item+".mp3"):
        print("İndirme tamamlandı.")
        driver.quit()
        file.close()
        break




