#!/usr/bin/python
# -*- coding: utf-8 -*-

# FetchFood
# Fetch menu data from page, structurize it and POST it to webserver.

import urllib2
import re
import time
import sys
import datehelper
import food
import post
import mail
import config
import passwd
from bs4 import BeautifulSoup

def generate_food_entries(date, soup):
    entrylist = []
    entrylist_special = []
    food_generator = food.FoodEntryGenerator(date)

    for p_tag in soup:
        plaintext = p_tag.contents[0].strip() #html -> plaintext
        entry = food_generator.generate_entry(plaintext)

        if entry is not None:
            if entry.hasinfo:
                entrylist_special.append(entry)
            else:
                entrylist.append(entry)

    for entry in entrylist_special:
        entry.info = food_generator.generated_info
        entrylist.append(entry)
    return entrylist

def round_time(time):
    return round(time, 2)

#####

exec_timekeys = ("total", "target_request", "generate_entries", "clear_table", "post_entry_all")
exec_times = dict.fromkeys(exec_timekeys, [0, 0])
exec_times["total"][0] = time.time()
exec_times["target_request"][0] = time.time()

try:
    page = urllib2.urlopen(config.TARGET_URL)
except urllib2.URLError as e:
    if config.CONFIG_MAIL_ENABLED:
        mailInfo("FetchFood ERROR!", "Error requesting GET to " + config.TARGET_URL + " ->\r" + str(e.reason))
    sys.exit(1)
except urllib2.HTTPError as e:
    if config.CONFIG_MAIL_ENABLED:
        mailInfo("FetchFood ERROR!", "Error requesting GET to " + config.TARGET_URL + " ->\r" + str(e.code) + ", " + str(e.reason))
    sys.exit(1)

exec_times["target_request"][1] = time.time() - exec_times["target_request"][0]

page_soup = BeautifulSoup(page)
page.close()
date_soup = page_soup.select("h2#" + config.DATE_INNER_ID)
date_plaintext = date_soup[0].contents[0].strip()
date = datehelper.find_date(date_plaintext)
content_soup = page_soup.select("div#" + config.CONTENT_OUTER_ID +
                                " div[class-=" + config.CONTENT_INNER_CLASS +
                                "] p")
exec_times["generate_entries"][0] = time.time()
entrylist = generate_food_entries(date, content_soup)
exec_times["generate_entries"][1] = time.time() - exec_times["generate_entries"][0]
exec_times["clear_table"][0] = time.time()
post.post(config.POST_URL, config.POST_PAGE, config.POST_HEADERS, passwd.POST_PASSWD, config.ACTION_CLEAR_TABLE) #Clear database table.
exec_times["clear_table"][1] = time.time() - exec_times["clear_table"][0]
exec_times["post_entry_all"][0] = time.time()
entrycount = post.post_entries(entrylist)
exec_times["post_entry_all"][1] = time.time() - exec_times["post_entry_all"][0]
exec_times["total"][1] = time.time() - exec_times["total"][0]

data = {}
for type_, time in exec_times.iteritems():
    data[type_] = time
post.post(config.POST_URL, config.POST_PAGE, config.POST_HEADERS, passwd.POST_PASSWD, config.ACTION_POST_INFO, data)

mail_content = "fetchfood.py successfully ran at:\n\n" + datehelper.current_date() + "\n\nEntries posted: " + str(entrycount) + "\nTotal execution time: " + str(round_time(exec_times["total"][1])) + "s" + "\n    Time getting menu: " + str(round_time(exec_times["target_request"][1])) + "s" + "\n    Time generating entries: " + str(round_time(exec_times["generate_entries"][1])) + "s" + "\n    Time clearing DB: " + str(round_time(exec_times["clear_table"][1])) + "s" + "\n    Time posting to DB: " + str(round_time(exec_times["post_entry_all"][1])) + "s"
print mail_content
if config.CONFIG_MAIL_ENABLED:
    mail.sendmail("FetchFood Completed!", mail_content)
sys.exit(0)
