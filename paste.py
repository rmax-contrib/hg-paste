#!/usr/bin/env python

'''send information from Mercurial to various pastebin websites
'''

from mercurial import util
from urllib2 import urlopen


def _paste_dpaste(**parameters):
    pass

pastebins = {
    'dpaste': { 'url': 'http://dpaste.com/api/v1/',
                'parameters': {
                    'required': ['code'],
                    'optional': ['title'], },
                'handler': _paste_dpaste,
    }
}

def paste(ui, repo, destination, **opts):
    if destination not in pastebins:
        raise util.Abort('Unknown pastebin.  See "hg help paste" for supported pastebins.')
        return
    
    


cmdtable = {
    "paste": 
    (paste, [
        ('d', 'destination', '', 'the pastebin site to use'),
        ('t', 'title', '', 'the title of the paste (optional)'),
    ],
    'hg paste -d PASTEBIN')
}