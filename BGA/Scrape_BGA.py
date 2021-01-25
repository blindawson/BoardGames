import requests
import bs4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

#
# res = requests.get('https://boardgamearena.com/gamestats?player=84034013')
#
# res.raise_for_status()
#
# playFile = open('bga_play_history.txt', 'wb')
# for chunk in res.iter_content(100000):
#     playFile.write(chunk)
#
# soup = bs4.BeautifulSoup(res.text, 'html.parser')
#
# soup.select('#gamelist_inner > tr:nth-child(1) > td:nth-child(1) > a > span.smalltext')

browser = webdriver.Chrome(r'C:\Users\bisfo\Desktop\chromedriver.exe')
browser.get('https://boardgamearena.com/gamestats?player=84034013')

see_more_link = browser.find_element_by_css_selector('#see_more_tables')
while True:
    try:
        if browser.find_element_by_css_selector('#head_infomsg_1 > div.head_infomsg_item'):
            print('no more results')
            break
    except NoSuchElementException:
        see_more_link.click()
        time.sleep(1)


game_name = browser.find_element_by_css_selector(
    '#gamelist_inner > tr:nth-child(1) > td:nth-child(1) > a').text.split('\n')[0]
date = browser.find_element_by_css_selector(
    '#gamelist_inner > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1)').text.split()[0]
duration = browser.find_element_by_css_selector(
    '#gamelist_inner > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2)').text
player_name = browser.find_element_by_css_selector(
    '#gamelist_inner > tr:nth-child(1) > td:nth-child(3) > div:nth-child(1) > div.name > a').text
player_score = browser.find_element_by_css_selector(
    '#gamelist_inner > tr:nth-child(1) > td:nth-child(3) > div:nth-child(1) > div.score').text
# browser.quit()