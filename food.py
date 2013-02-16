import datecheck
import config

class FoodEntry:

    def __init__(self, date, type_, content, hasinfo=False, info=""):
        self.date = date
        self.type_ = type_
        self.content = content
        self.hasinfo = hasinfo
        self.info = info

    def __eq__(self, other):
        if (self.date == other.date and
            self.type_ == other.type_ and
            self.content == other.content and
            self.info == other.info):
            return True
        else:
            return False

    def get_data(self):
        return {"date" : self.date.encode("utf-8"),
                "type" : self.type_.encode("utf-8"),
                "content" : self.content.encode("utf-8"),
                "info" : self.info.encode("utf-8")}

class FoodEntryException(Exception):

    def __init__(self, exception):
        self.exception = exception

class FoodEntryGenerator:

    REGEX_TYPE = r".+?(?=\s*[A-ZÅÄÖ])"      #matches Lunch, Soppa, etc
    REGEX_WEEK = r"v\.\d{1,2}$"             #matches v.3, v.24, etc
    REGEX_INFO = r"^\*=.+$"                 #matches *=innehåller fläskött, etc
    REGEX_GOODMEAL = r"^Smaklig.*"          #matches Smaklig Måltid
    REGEX_WHITESPACE = r"^$"                #matches ""

    def __init__(self, init_date):
        self.date = init_date
        self.weekday = 0
        self.generated_info = None

    def increase_day_by(self, amount):
        self.weekday += amount

    def generate_entry(entry_string):
        new_weekday = datehelper.is_weekday(entry_string, self.weekday)
        if new_weekday != self.weekday:
            self.weekday = new_weekday
            self.date = datehelper.weekday_to_date(init_date, self.weekday)
            return

        elif (not re.match(REGEX_WEEK, entry_string)
            and not re.match(REGEX_GOODMEAL, entry_string)
            and not re.match(REGEX_WHITESPACE, entry_string)
            and not re.match(REGEX_INFO, entry_string)):
            typeobject = re.match(REGEX_TYPE, entry_string)

            if typeobject is not None:
                try:
                    type_ = typeobject.group().strip()
                except AttributeError:
                    type_ = config.FOOD_UNKNOWN_TYPE
            else:
                type_ = config.FOOD_DEFAULT_TYPE

            content = entry_string.replace(type_, "").strip()

            if "*" in content:
                return FoodEntry(date, type_, content.replace("*", ""), True))
            else:
                return FoodEntry(date, type_, content, False))

        elif re.match(REGEX_INFO, entry_string):
            self.info = re.match(REGEX_INFO, entry_string).group().replace("*=", "").strip()

        #elif (not re.match(REGEX_INFO, entry_string)
        #    and not re.match(REGEX_WHITESPACE, entry_string)):
         #   type_ = config.FOOD_DEFAULT_TYPE
          #  content = entry_string.replace(type_, "").replace("*", "").strip()

           # return
