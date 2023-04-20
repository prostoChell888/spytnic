class DateTime:
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def is_equal(self, datetime):
        return (datetime.year == self.year) and (datetime.month == self.month) and (datetime.day == self.day) and (datetime.hour == self.hour) and(datetime.minute == self.minute) and (datetime.second == self.second)

    def time_to_string(self):
        res = str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)
        return res

    def date_to_string(self):
        res = str(self.day) + "." + str(self.month) + "." + str(self.year)
        return res

