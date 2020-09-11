# Helper.py
# Michael Cole
#
# A collection of minor helper methods that can be
# used throughout the app
# ------------------------------------------------

from datetime import datetime


class Helper:
    '''
    Helper Class that provides minor helper methods
    '''

    def getGreeting(self):
        '''
        Returns a greeting based on the time of day
        '''
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
        '''
        Gets local time for a given timezone
        '''
        import pytz

        utc_now = pytz.utc.localize(datetime.now())
        return utc_now.astimezone(pytz.timezone(tz))

    def chunk(self, thelist, maxNumElements):
        '''
        A generator which chunks a given list into a list with
        sublists. Each sublist contains no greater than
        maxNumElements elements

        Ex: chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
        '''
        for idx in range(0, len(thelist), maxNumElements):
            yield thelist[idx:idx + maxNumElements]
