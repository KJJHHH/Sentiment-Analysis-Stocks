from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup

import sys
import requests
import json
import datetime


def onStart():
    suffix_output = "HW_2_begin.json"
    currentDT = datetime.datetime.now()
    dictfilename = currentDT.strftime("%Y%m%d%H_") + suffix_output
    print('[onStart]: ', dictfilename)
    json_file = open(dictfilename, 'w')
    return json_file

def onStop(json_file):
    json_file.close()

def process_item(json_file, item):
    line = json.dumps(dict(item),ensure_ascii=False) + "\n"
    json_file.write(line)

    return item

def get_selenium():                           
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('headless')                        
    driver = webdriver.Chrome(chrome_options=options)
    return (driver)

def get_level_2(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # 做一點什麼別的，把目標本文抓好
    # contents = soup.find( 'div', { 'class': 'whitecon' } )
    # body > main > div > section.wrapper-left.main-content__wrapper > section > article
    contents = soup.find("div", {"class": "_2E8y"})
    time = soup.find("time").text
    content = ""
    if contents:
        parags = contents.find_all("p")
        for i, parag in enumerate(parags):
            if not parag.has_attr("class") and parag.string is not None or not parag.findChild('a') :
                content += parag.string   
    return content, time

def snapshot_page_source(checkpoint, driver):
    # Storing the page source in page variable
    page = driver.page_source.encode('utf-8')
    # print(page)
  
    # create result.html
    toFile = "snapshot_%s.html"%(checkpoint)
    file_ = open(toFile, 'wb')
  
    # Write the entire page content in result.html
    file_.write(page)
  
    # Closing the file
    file_.close()

def main(delay_time, search):
    '''
    Start to crawl a webpage, and using beautifulsoup
    '''

    data_json = onStart()
    start_url = f"https://www.cnyes.com/search/news?keyword={search}"
    driver = webdriver.Chrome()
    driver.get(start_url)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    # my variables
    counter_i = 0
    max_tried = 10
    last_snapshot = 0
    # Use url as key
    dict_unipost = dict()

    while True:

        try:
            # check current elements/time

            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Process the page so far
            sleep(delay_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            # data-ad-comet-preview and data-ad-preview
            level_1_list = driver.find_elements(by=By.XPATH, value='//div[@data-ad-comet-preview="message" and @data-ad-preview="message"]')
                            
            article_links = []
            for element in level_1_list:
                a_item = dict()
                article_link = element.get_attribute("href")
                article_links.append(article_link) if article_link is not None else None
            
            for article_link in article_links:
                content, time = get_level_2(article_link)


            print('-'*80)
            # Another approach

            # Calculate new scroll height and compare with last scroll height
            #new_height = driver.execute_script("return document.body.scrollHeight")
            #if new_height == last_height:
            #    break
            #last_height = new_height

        except KeyboardInterrupt:
            print('Got KeyboardInterrupt, will break out of the loop.')
            break
        except NoSuchElementException:
            print('Cannot locate child element, continue...')
            continue


    print("--------- The crawl task has been DONE ------------")
    onStop(data_json)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: %s <delay seconds>"%sys.argv[0])
        sys.exit(1)

    if sys.argv[1]:
        main(int(sys.argv[1]), search="友達")

