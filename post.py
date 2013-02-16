import urllib
import config

def post(url, page, headers, action, data={}):
    data['action'] = action
    data_encoded = urllib.urlencode(data)
    connection = httplib.HTTPConnection(url)

    try:
        connection.request("POST", page, data_encoded, headers)
    except httplib.HTTPException as e:
        if config.CONFIG_MAIL_ENABLED:
            mailInfo("FetchFood ERROR!", "Error requesting POST to " + url + page + " ->\rHTTPError")
        connection.close()
        sys.exit(1)
    response = connection.getresponse()
    response_data = response.read().trim()

    if not (int(response_data[0]) == 0 and int(response_data[1]) == 0):
        sendmail("FetchFood ERROR!", "Error requesting POST to " + url + page + " ->\r" + response_data)

    return True

def post_entries(entrylist):
    entrycount = 0
    for entry in entrylist:
        postdata = entry.get_data();
        try:
            post(config.POST_URL, config.POST_PAGE, config.POST_HEADERS, config.ACTION_POST_FOOD, postdata)
        except FoodEntryException as e:
            if config.CONFIG_MAIL_ENABLED:
                sendmail("FetchFood ERROR!", "Error generating entries ->\r" + str(e.exception))
            sys.exit(1)
        else:
            entrycount += 1

    return entrycount
