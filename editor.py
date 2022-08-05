#!/bin/env python3

import datetime
import os
import string
import subprocess
import time

"""Module docstring"""

WIDTH=53
HEIGHT=7


class CommitEditor:

    TAGNAME = 'commit-editor-start-0'
    DEPTH = {'.': 1,
             '=': 51,
             '+': 101,
             '*': 151}

    def __init__(self, pattern):
        self.pattern = str(pattern).replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
        self.currentDir = os.path.dirname(os.path.realpath(__file__))

        if len(self.pattern) != WIDTH * HEIGHT:
            raise Exception('Pattern must be %s by %s not %d' % (WIDTH, HEIGHT, len(self.pattern)))

        self.transposePattern()

    def transposePattern(self):
        """Transposes the pattern for easier manipulation later"""
        p = ''
        for i in range(WIDTH):
            for j in range(HEIGHT):
                p+=self.pattern[i+j*WIDTH]

        self.pattern = p

    def initialiseGit(self):
        """Initialise the git repo stuff"""
        with open('/dev/null', 'w') as devNull:
            subprocess.check_call('cd %s && cp editor.py README.md ../' % (self.currentDir), shell=True, stdout=devNull)
            subprocess.call('cd %s && git reset --hard %s' % (self.currentDir, self.TAGNAME), shell=True, stdout=devNull)
            subprocess.check_call('cd %s && mv ../editor.py ../README.md .' % (self.currentDir), shell=True, stdout=devNull)
            subprocess.call('cd %s && git tag -d %s' % (self.currentDir, self.TAGNAME), shell=True, stdout=devNull)
            subprocess.check_call('cd %s && git add editor.py README.md' % self.currentDir, shell=True, stdout=devNull)
            subprocess.check_call('cd %s && git commit -m "Started editor"' % self.currentDir, shell=True, stdout=devNull)
            subprocess.check_call('cd %s && git tag %s' % (self.currentDir, self.TAGNAME), shell=True, stdout=devNull)

    def dateRange(self, startDate, endDate):
        """Date range iterator in steps of one date"""
        for n in range((endDate-startDate).days):
            yield startDate + datetime.timedelta(n)

    def getDateAYearAgoSunday(self):
        """Gets the date a year ago last sunday"""
        d = datetime.date.fromtimestamp(time.time() - WIDTH*HEIGHT*24*60*60)
        
        while d.weekday() != 6:
            d = d - datetime.timedelta(days=1)

        return d

    def createCommits(self):
        """Create the commits to make the pattern"""
        self.initialiseGit()
        aYearAgo = self.getDateAYearAgoSunday()
        
        for i, date in enumerate(self.dateRange(aYearAgo, datetime.date.today())):
            pixel = '.' if i >= len(self.pattern) else self.pattern[i]
            for _ in range(self.DEPTH[pixel]):
                # do commits
                with open('/dev/null', 'w') as devNull:
                    subprocess.check_call('cd %s && git commit -m "editing" --allow-empty --date %sT12:00:00' % (self.currentDir, date), shell=True, stdout=devNull)

if __name__ == '__main__':
    ptrn = """
. . = + * + = . . . . . . . = + + + = . . . . = + + + = . . . . = + + + = . . . . . . . . . * * . . . . .
. = + * * * + = . . . . . = . . + . . = . . = . . + . . = . . = . . + . . = . . . . . . * * * . . . . . .
. + * * * + . . . . . . . + . * + . * + . . + . * + . * + . . + . * + . * + . . . . . * . * . . . . . . .
. * * * . . . . . . . . . + . . + . . + . . + . . + . . + . . + . . + . . + . . . + * + . + . . . . . . .
. + * * * + . . . . . . . + + + + + + + . . + + + + + + + . . + + + + + + + . . . * * * = + = . . . . . .
. = + * * * + = . . . . . + + = + + = + . . + + = + + = + . . + + = + + = + . . . + * + = + * . . . . . .
. . = + * + = . . . . . . + . . + . . + . . + . . + . . + . . + . . + . . + . . . . . . = * + . . . . . ."""

    ce = CommitEditor(ptrn)

    ce.createCommits()

    print('To see the results, push to github use\ngit push --tags origin master')