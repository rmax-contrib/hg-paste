#!/usr/bin/env python

'''send information from Mercurial to various pastebin websites
'''

import urllib2
from urllib import urlencode
from mercurial import util


def _paste_dpaste(content, **parameters):
    data = [('content', content)]
    if parameters['title']:
        data.append(('title', parameters['title']),)
    if parameters['user']:
        data.append(('poster', parameters['user']),)
    data = urlencode(data)
    
    request = urllib2.Request(pastebins['dpaste']['url'], data)
    response = urllib2.urlopen(request)
    
    location = response.geturl()
    return location

pastebins = {
    'dpaste': { 'url': 'http://dpaste.com/api/v1/',
                'parameters': {
                    'required': ['content'],
                    'optional': ['title', 'user'], },
                'handler': _paste_dpaste,
    }
}

def paste(ui, repo, destination, **opts):
    if destination not in pastebins:
        raise util.Abort('Unknown pastebin.  See "hg help paste" for supported pastebins.')
    
    if not opts['user']:
        opts['user'] = ui.username()
    
    url = pastebins[destination]['handler'](content='testing with urllib2', **opts)
    ui.write('%s\n' % url)


cmdtable = {
    "paste": 
    (paste, [
        ('d', 'destination', '', 'the pastebin site to use'),
        ('t', 'title', '', 'the title of the paste (optional)'),
        ('u', 'user', '', 'the name of the paste\'s author (defaults to the '
                          'username configured for Mercurial)'),
    ],
    'hg paste -d PASTEBIN')
}