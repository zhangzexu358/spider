from selenium import webdriver
import time
import os
from selenium.webdriver.support.ui import WebDriverWait

def getDriver(type):
    driver = None
    try:
        path = os.path.abspath('..')

        if type == "chrome":
            file_name = "chromedriver.exe"
            driver_path = path + "\\" + file_name
            driver = webdriver.Chrome(driver_path)
    except:
        path = os.path.abspath(os.curdir)
        if type == "chrome":
            file_name = "chromedriver.exe"
            driver_path = path + "\\spiderV1\\" + file_name
            driver = webdriver.Chrome(driver_path)

    return driver

if __name__ == '__main__':
    driver = getDriver("chrome")
    driver.get("https://bbs.scol.com.cn/home.php?mod=myspace")
    time.sleep(2)
    wait = WebDriverWait(driver, 10)  # 指定元素加载超时时间
    driver.set_page_load_timeout(30)  # 页面加载超时时间

    print(driver.get_cookies())
