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
from bs4 import BeautifulSoup



def GetLikes(driver,url):
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div #bottom-row")))      
    elements = driver.find_elements(By.CSS_SELECTOR, "div .yt-core-attributed-string--white-space-no-wrap")
    elements = [element.text for element in elements]
    if 'Join' in elements:
        video_likes = str(elements[5])
    else:
        video_likes = str(elements[4])
    video_likes = ConvertToInt(video_likes)

    return video_likes

def ConvertToInt(string):
    if "M" in string:
        string = int(float(string[0 : string.index("M")]) * 1000000)
    elif "K" in string:
        string = int(float(string[0 : string.index("K")]) * 1000)
    else:
        string = int(string)

    return string