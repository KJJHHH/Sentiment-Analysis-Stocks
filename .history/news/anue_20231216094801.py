from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService
from pathlib import Path

import sys
import requests
import json
import datetime
import warnings
# Suppress the DeprecationWarning
warnings.simplefilter("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")


def onStart(search):
    suffix_output = f"anue_{search}.json"
    currentDT = datetime.datetime.now()
    dictfilename = currentDT.strftime("%Y%m%d%H_") + suffix_output
    print('[onStart]: ', dictfilename)
    json_file = open(f"texts/{dictfilename}", 'w', encoding="utf-8", errors="replace")
    return dictfilename, json_file

def onStop(json_file):
    json_file.close()

def get_item(filename):
    # file_path = 'C:/Users/USER/Desktop/sentiment_Text/news/texts/2023121521_anue_友達.json'
    json_file = open(f"texts/{filename}", 'r', encoding="utf-8", errors="replace")
    dict_posts = json.load(json_file)
    return dict_posts, json_file

def process_item(json_file, data):
    line = json.dumps(data, indent=2, ensure_ascii=False)
    json_file.write(line)

def get_selenium():                           
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('headless')                        
    driver = webdriver.Chrome('C:/Users/USER/Desktop/sentiment_Text/news/chromedriver.exe', 
                              chrome_options=options)
    return driver

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
            if not parag.has_attr("class") and parag.string is not None:
                content += parag.string  
    if content == "":
        content = soup.find("h1").text
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
    
    #########################################
    ## How to fix the certificate warnings 
    ## https://www.guru99.com/ssl-certificate-error-handling-selenium.html
    ## https://www.google.com/search?q=certificate+error+chrome+in+selenium&sca_esv=591191718&rlz=1C1GCEA_enTW920TW920&sxsrf=AM9HkKlbYAxsVAOsgEGaPcX3DBta2iMmrg%3A1702643518078&ei=Pkd8ZeGwBIePvr0P56CtiAM&oq=certificate+error+chrome+in+selel&gs_lp=Egxnd3Mtd2l6LXNlcnAiIWNlcnRpZmljYXRlIGVycm9yIGNocm9tZSBpbiBzZWxlbCoCCAEyBxAhGKABGAoyBxAhGKABGAoyBxAhGKABGApIgSNQxwdY1hZwAXgBkAEBmAH2BaABxRmqAQc0LTMuMi4xuAEDyAEA-AEBwgIKEAAYRxjWBBiwA8ICBRAhGKAB4gMEGAAgQYgGAZAGCg&sclient=gws-wiz-serp
    #########################################
    filename = '2023121521_anue_友達.json'
    path = f'C:/Users/USER/Desktop/sentiment_Text/news/texts/{filename}'
    if Path(path).exists():
        print(f"The file or directory at {path} exists.")
        dict_posts, data_json = get_item(filename)
    else:
        print(f"The file or directory at {path} does not exist.")
        filename, data_json = onStart(search)
        dict_posts = dict()

    start_url = f"https://www.cnyes.com/search/news?keyword={search}"
    driver = get_selenium()
    driver.get(start_url)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    # my variables
    counter_i = 0
    max_tried = 10
    last_snapshot = 0
    stop = False
    # data variables
    stop_date = datetime.datetime(2020, 1, 1)

    n_tryexcept = 0
    while True:
        try:
            # check current elements/time
            print(f"Implement Time: {datetime.datetime.now()}")

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
            level_1_list = driver.find_elements(by=By.CLASS_NAME, value="jsx-1986041679") # class 2: "news"
            new_article = []
            for element in level_1_list:
                article_link = element.get_attribute("href")
                if article_link is not None and article_link not in dict_posts:
                    new_article.append(article_link)

            if new_article == []:
                print("No text from this scroll")
            
            for article_link in new_article:
                try:
                    content, time = get_level_2(article_link)
                    dict_posts[article_link] = [time, content]
                    time = datetime.datetime.strptime(time, "%Y/%m/%d %H:%M")
                    process_item(data_json, dict_posts)
                    print('-'*80)
                    if time <= stop_date:
                        stop = True
                        break
                except:
                    print(f"Get no texts from the url: {article_link} !!!!!")
                
            if stop == True:
                break            
            
            n_tryexcept = 0

        except KeyboardInterrupt:
            print('Got KeyboardInterrupt, will break out of the loop.')
            break
        except NoSuchElementException:
            print('Cannot locate child element, continue...')
            n_tryexcept += 1
            if n_tryexcept >= max_tried:
                break
            else:
                continue
        


    print("--------- The crawl task has been DONE ------------")
    onStop(data_json)


if __name__ == "__main__": 
    ##################################################
    ########## To run the anue.py code ###############
    # cd C:/Users/USER/Desktop/sentiment_pc/news
    # py -3.10 anue.py 3 友達    
    ##################################################
    
    if (len(sys.argv) < 2):
        print("Usage: %s <delay seconds>"%sys.argv[0])
        sys.exit(1)

    if sys.argv[1]:
        main(int(sys.argv[1]), sys.argv[2])

