#!/usr/bin/env python

'''send information from Mercurial to various pastebin websites
'''

from mercurial import util

pastebins = {
    'dpaste': 'http://dpaste.com/api/v1/'
}

def paste(ui, repo, destination, **opts):
    if destination not in pastebins:
        raise util.Abort('Unknown pastebin.  See "hg help paste" for supported pastebins.')
        return
    pass


cmdtable = {
    "paste": 
    (paste, [
        ('d', 'destination', '', 'the pastebin site to use'),
    ],
    'hg paste -d PASTEBIN')
}