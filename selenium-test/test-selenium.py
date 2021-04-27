from selenium import webdriver
from scrapy import Selector

driver_path = '/usr/local/chromedriver/chromedriver'


chrome_options = webdriver.ChromeOptions()
opts = [
    '--headless',                           # do not display the browser
    '--disable-gpu',
    '--disable-extensions',                 # 禁止插件
    '-blink-settings=imagesEnabled=false',  # 不加载图片
]

for opt in opts:
    chrome_options.add_argument(opt)

chrome = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
chrome.get('http://quotes.toscrape.com/tag/humor/')
source_page = chrome.page_source

sel = Selector(text=source_page)




