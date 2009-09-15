#!/usr/bin/env python

'''send information from Mercurial to various pastebin websites'''

def paste(ui, repo, destination=None, **opts):
    pass


cmdtable = {
    "paste": 
    (paste, [
        ('d', 'destination', None, 'the pastebin site to use'),
    ],
    'hg paste --destination PASTEBIN')
}