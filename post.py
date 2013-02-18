import urllib
import httplib
import mail
import config
import passwd

class PostException(Exception):

    def __init__(self, type_, exception, url):
        self.type_ = type_
        self.exception = exception
        self.url = url

    def __str__(self):
        return self.type_ + ": " + self.exception + " -> " + self.url

def post(action, data={}):
    data["passwd"] = passwd.POST_PASSWD
    data["action"] = action
    data_encoded = urllib.urlencode(data)
    connection = httplib.HTTPConnection(config.POST_URL)

    try:
        connection.request("POST", config.POST_PAGE, data_encoded, config.POST_HEADERS)
    except httplib.HTTPException as e:
        raise PostException("HTTP", e, config.POST_URL + config.POST_PAGE)
        connection.close()
        sys.exit(1)
    response = connection.getresponse()
    response_data = response.read().replace("\n", "").strip()
    try:
        response_code = int(response_data[0] + response_data[1])
    except ValueError:
        raise PostException("PORTALN.SE", "Internal server error", config.POST_URL + config.POST_PAGE)

    if response_code != 0:
        raise PostException("FOODAPI", response_data, config.POST_URL + config.POST_PAGE)
    return True

def post_entries(entrylist):
    entrycount = 0
    for entry in entrylist:
        postdata = entry.get_data();
        try:
            post(config.ACTION_POST_FOOD, postdata)
            entrycount += 1
        except PostException:
            raise
    return entrycount
