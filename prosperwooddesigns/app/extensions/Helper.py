from datetime import datetime


class Helper:

    def getGreeting(self):
        ct_now = self.getTime_tz()
        hour = ct_now.time().hour

        if hour >= 4 and hour <= 11:
            return 'Good Morning'
        elif hour >= 12 and hour <= 16:
            return 'Good Afternoon'
        elif hour >= 17 and hour <= 23:
            return 'Good Evening'
        else:
            return 'It is very late'

    def getTime_tz(self, tz='America/Chicago'):
        import pytz

        utc_now = pytz.utc.localize(datetime.now())
        return utc_now.astimezone(pytz.timezone(tz))
