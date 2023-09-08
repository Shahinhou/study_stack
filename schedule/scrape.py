#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


s = input("Course Name: ")
today = str(datetime.datetime.now()).split()[0]
print(today)
today = '2023-9-11'

url = f"https://mytimetable.dcu.ie/timetables?date={today}&view=week&timetableTypeSelected=241e4d36-60e0-49f8-b27e-99416745d98d"
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options) #options=options)

driver.implicitly_wait(10)
driver.get(url) #+"&searchText=comsci2")

print(driver.title)

search_bar = driver.find_elements(By.ID, "mat-input-0")[0]
print(driver.current_url)

search_bar.clear()
search_bar.send_keys(s)
search_bar.send_keys(Keys.RETURN)
print(driver.current_url)

table_url = driver.current_url

driver.implicitly_wait(10)
#driver.get(table_url)

box = driver.find_elements(By.TAG_NAME, "mat-pseudo-checkbox")[0]
print(box)
box.click()

print(driver.current_url)

box = driver.find_elements(By.CLASS_NAME, "e-appointment")
print(box)
for s in box:
    lesson,b = (s.get_attribute('aria-label')).split(maxsplit=1)
    print(lesson)
    #print(b)

    #p1 = 'Begin From '
    #c = re.sub(p1, '', b[0])

    day = b.split()[2]
    print(day)
    p2 = r'\d*\d:\d\d:\d\d'
    begin, end = re.findall(p2, b)
    print(begin, end)
    

