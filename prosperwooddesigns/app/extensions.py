import sys


class Logger:

    def log(self, string, loc='stdout'):
        if loc == 'stdout':
            print(f'>> {string}', file=sys.stdout, flush=True)
        else:
            print(f'>> {string}', file=loc, flush=True)
