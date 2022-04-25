import requests
import bs4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd

service = webdriver.chrome.service.Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

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

browser.get("https://boardgamearena.com/gamestats?player=84034013")
time.sleep(20)

# see_more_link = browser.find_element_by_css_selector('#see_more_tables')
# while True:
#     try:
#         if browser.find_element_by_css_selector('#head_infomsg_1 > div.head_infomsg_item'):
#             print('no more results')
#             break
#     except NoSuchElementException:
#         see_more_link.click()
#         time.sleep(1)

df = pd.DataFrame([], columns=["Game", "Datetime", "Duration", "Players"])

table = browser.find_element(
    by=webdriver.common.by.By.XPATH, value='//*[@id="gamelist_inner"]'
)
rows = table.find_elements(by=webdriver.common.by.By.TAG_NAME, value="tr")


def read_row(df, row):
    row = row.text.split("\n")
    [game_name, log_id, date_played, duration] = row[:4]
    players = row[4:-3]
    df2 = pd.DataFrame(
        {
            "Game": game_name,
            "Datetime": date_played,
            "Duration": duration,
            "Players": [players],
        },
        index=[log_id],
    )
    return pd.concat([df, df2])


for row in rows:
    df = read_row(df, row)

df['Duration'] = df['Duration'].apply(lambda x: int(x[:-4]))
# Remove dates that say an hour ago or yesterday or something
# Convert datetime to separate date and time categories
# Postprocess players to line up with Upload_BGG.py
# We need a dictionary of BGG game ids
print(df)

# browser.quit()
