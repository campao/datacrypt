#coding: utf-8
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time


browser = webdriver.Safari()
browser.get("https://twitter.com/search?q=(%23bitcoin)%20until%3A2012-02-01%20since%3A2012-01-01&src=typed_query")
wait = WebDriverWait(browser, 100)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'js-stream-item.stream-item.stream-item')));
for elm in browser.find_elements_by_css_selector("js-stream-item.stream-item.stream-item"):
    print(elm.text)
