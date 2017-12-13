#-*- coding:utf-8 -*-
from selenium import webdriver
import os
import time

#截图函数
def insert_img(driver,file_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace("\\","/")
    base = base_dir.split('/test_case')[0]
    file_path = base + "/report/image/" + file_name
    driver.save_screenshot(file_path)
    # driver.get_screenshot_as_file()

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("http://www.baidu.com")
    insert_img(driver,'baidu111111111111111.png')
    driver.quit()