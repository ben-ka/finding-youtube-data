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
import datetime
from flask import Flask,abort,jsonify, request


app = Flask(__name__)
@app.route('/videos/<channel>', methods = ['GET'])

def Get_video_details(channel):
    try:
        if "@" in channel:
            is_full = True
        else:
            is_full = False
        chrome_driver_path = r"C:/Development/chromedriver_win32/chromedriver.exe"
        chrome_options = Options() #Create a Options class, necessarly to keep open the Chrome Browser
        chrome_options.add_experimental_option("detach", True)

        chrome_options.add_argument("--lang=en-us") 
        # chrome_options.add_argument("--headless")
        
        service = Service(executable_path=chrome_driver_path) #Create a Service class to handle the driver
        
        driver = webdriver.Chrome(service=service, options=chrome_options)


        driver.maximize_window()
        if is_full:
            driver.get(f'https://www.youtube.com/{channel}/videos')
        else:
            driver.get(f'https://www.youtube.com/@{channel}/videos')



        time.sleep(2)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "video-title-link")))
        except:
            return jsonify({'message': 'It appears there isnt a youtube channel with the name specified, please check your spelling and make sure you put a "@" before the channel name'}), 404
        keep_going = True
        count = 0
        prev_last_link = None
        while keep_going:
            last_link = driver.find_elements(By.ID, "video-title-link")[-1].get_attribute('href')
            driver.execute_script(f'window.scrollBy(0, 3000);')
            
            time.sleep(0.5)
            if last_link == prev_last_link:
                keep_going = False
            prev_last_link = last_link
            
        video_links = driver.find_elements(By.ID,"video-title-link")

        video_links = [video.get_attribute('href') for video in video_links]


        video_names = driver.find_elements(By.ID,"video-title-link")
        video_names = [video.get_attribute('title') for video in video_names]

        video_images = driver.find_elements(By.CLASS_NAME,"yt-core-image--loaded")
        video_images = [video.get_attribute('src') for video in video_images]

        video_meta = driver.find_elements(By.CSS_SELECTOR,"div #metadata-line span")
        video_meta = [video.text for video in video_meta]
        video_time = video_meta[1::2]
        video_meta = video_meta[0::2]
        video_views = video_meta

        driver.quit()

        all_videos = []
        for i in range(len(video_links)):
            video = {}
            video['id'] = i+1
            try:
                video['url'] = video_links[i]
            except:
                video['url'] = ""
            try:
                video['title'] = video_names[i]
            except:
                video['title'] = ""
            try:
                video['age'] = video_time[i]
            except:
                video['age'] = ""
            try:
                video['views'] = video_views[i]  
            except:
                video['views'] = ""
            try:
                video['thumbnail'] = video_images[i]
            except:
                video['thumbnail'] = ''
            
            all_videos.append(video)
        user_videos = {f'{channel.strip("@")} videos': all_videos}


        file = f'video_data-{channel.strip("@")}.csv'
        sys.stdout = open(file, 'w',encoding='utf-8')
        pd.DataFrame(user_videos).to_csv(sys.stdout,header=True,index=False,encoding='utf-8')   
        sys.stdout = sys.__stdout__
        response = jsonify(user_videos)
        # response.headers["Content-Type"] = "application/json; charset=utf-8"  # Set the Content-Type to include utf-8 encoding
        # response.headers["Access-Control-Allow-Origin"] = "*"  # Allow cross-origin requests, if needed
        return response, 200
    except:
        return jsonify({'message': 'there has been an error'}),400


if __name__ == '__main__':
    app.run(debug=True)

    
