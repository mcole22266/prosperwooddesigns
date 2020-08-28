# Logger.py
# Michael Cole
#
# Used for logging -- both to the console and to log files
# --------------------------------------------------------

import os
import sys

from flask import current_app

from .Helper import Helper


class Logger:
    '''
    Logger object used to print to the console as well
    as log to a file in development
    '''

    helper = Helper()

    def log(self, string):
        '''
        Create a log. Based on environment variables, the logs will be
        written to stdout and/or a logfile
        '''
        if current_app.config['LOG_TO_STDOUT']:
            print(f'>> {string}', file=sys.stdout, flush=True)

        if current_app.config['LOG_TO_FILE']:
            # Get timestamp information
            now = self.helper.getTime_tz()
            year = str(now.year).rjust(4, '0')
            month = str(now.month).rjust(2, '0')
            day = str(now.day).rjust(2, '0')
            hour = str(now.hour).rjust(2, '0')
            minute = str(now.minute).rjust(2, '0')
            second = str(now.second).rjust(2, '0')

            # Define filename prefix
            fileprefix = f'/prosperwooddesigns/logs/{year}/{month}'
            if not os.path.exists(fileprefix):
                os.makedirs(fileprefix)

            # Define filename and timestamp
            filename = f'{fileprefix}/log_{year}{month}{day}.log'
            timestamp = f'{hour}:{minute}:{second}'

            # Write Log
            with open(filename, 'a+') as f:
                print(f'>> [{timestamp}] {string}', file=f, flush=True)
