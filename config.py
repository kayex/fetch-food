# -*- coding: utf-8 -*-
TARGET_URL = "http://www.amica.se/nackagymnasium"
TARGET_CONTENT_OUTER_IDENTIFIER = "div#ctl00_RegionPageBody_RegionPage_RegionContent_RegionMainContent_RegionMainContentMiddle_MainContentMenu_ctl00_MenuUpdatePanel"
TARGET_CONTENT_INNER_IDENTIFIER = "div[class-=ContentArea]"
TARGET_DATE_IDENTIFIER = "h2#ctl00_RegionPageBody_RegionPage_RegionContent_RegionMainContent_RegionMainContentMiddle_MainContentMenu_ctl00_HeadingMenu"

FOOD_DEFAULT_TYPE = u"Extrarätt"
FOOD_UNKNOWN_TYPE = "UNKNOWN_TYPE"

ACTION_POST_FOOD = "post_food"
ACTION_POST_INFO = "post_info"
ACTION_CLEAR_TABLE = "clear_table"

ERROR_CLEAR_TABLE_FATAL = True
ERROR_POST_ENTRY_FATAL = True
ERROR_POST_INFO_FATAL = False

POST_TYPE_TYPE = "type"
POST_TYPE_TIME = "time"

POST_URL = "www.portaln.se:80"
POST_PAGE = "/skola/foodapi.php"
POST_HEADERS = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

EMAIL_SERVER = "send.one.com:2525"
EMAIL_USER = "server@jvester.se"
EMAIL_FROM = "server@jvester.se"
EMAIL_TO = "jv@jvester.se"

CONFIG_MAIL_ENABLED = False
CONFIG_MAIL_NEWLINE = "\r"
