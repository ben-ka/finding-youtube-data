from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import pandas as pd
import sys

AMOUNT_OF_VIDEOS = 727
chrome_driver_path = r"C:/Development/chromedriver_win32/chromedriver.exe"
chrome_options = Options() #Create a Options class, necessarly to keep open the Chrome Browser
chrome_options.add_experimental_option("detach", True)
 
service = Service(executable_path=chrome_driver_path) #Create a Service class to handle the driver
 
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.maximize_window()
driver.get('https://www.youtube.com/@MrBeast/videos')


time.sleep(15)
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "video-title-link")))
keep_going = True
count = 0
while keep_going:
    
    driver.execute_script(f'window.scrollBy(0, 3000);')
    count += 1
    time.sleep(1)
    if count > 27:
        keep_going = False
    
video_links = driver.find_elements(By.ID,"video-title-link")

video_links = [video.get_attribute('href') for video in video_links]


video_names = driver.find_elements(By.ID,"video-title-link")
video_names = [video.get_attribute('title') for video in video_names]


video_meta = driver.find_elements(By.CSS_SELECTOR,"div #metadata-line span")
video_meta = [video.text for video in video_meta]
video_time = video_meta[1::2]
video_meta = video_meta[0::2]
video_views = video_meta



all_videos = []
for i in range(len(video_links)):
    video = {}
    video['url'] = video_links[i]
    video['title'] = video_names[i]
    video['age'] = video_time[i]
    video['views'] = video_views[i]   
    all_videos.append(video)


file = 'video_data.csv'
sys.stdout = open(file, 'w', encoding='utf-8')
pd.DataFrame(all_videos).to_csv(sys.stdout,header=True,index=False,encoding='utf-8')
    
driver.quit()
sys.stdout = sys.__stdout__