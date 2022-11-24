#coding: utf-8

from selenium.webdriver.common.by import By
from selenium import webdriver
import time

website = "https://careers.lse.ac.uk/events/emailbook/803087?token=c9V7biUiyO0WScFP7pGJYQ2&sessionId=13993"

driver = webdriver.Safari()
driver.get(website)
while driver.find_element(By.XPATH, "//*[contains(text(), 'unable')]"):
    time.sleep(2)
    driver.get(website)
else:
    print("event booked!")
    driver.quit()