#!/usr/bin/env python

'''send information from Mercurial to various pastebin websites
'''

import urllib2
from mercurial import cmdutil, commands, help, patch, util
from urllib import urlencode


def _paste_dpaste(content, **parameters):
    data = [('content', content), ('language', 'Diff')]
    if parameters['title']:
        data.append(('title', parameters['title']),)
    if parameters['user']:
        data.append(('poster', parameters['user']),)
    if parameters['keep']:
        data.append(('hold', 'on'),)
    data = urlencode(data)
    
    request = urllib2.Request(pastebins['dpaste']['url'], data)
    response = urllib2.urlopen(request)
    
    location = response.geturl()
    return location

pastebins = {
    'dpaste': { 'url': 'http://dpaste.com/api/v1/',
                'parameters': {
                    'required': ['content'],
                    'optional': ['title', 'user', 'keep', 'syntax'], },
                'handler': _paste_dpaste,
    }
}

def paste(ui, repo, *fnames, **opts):
    dest = opts.pop('dest')
    if not dest:
        dest = 'dpaste'
    if dest not in pastebins:
        raise util.Abort('unknown pastebin (see "hg help pastebins")!')
    
    if not opts['user']:
        opts['user'] = ui.username().replace('<', '').replace('>', '')
    
    ui.pushbuffer()
    if opts['rev']:
        revs = cmdutil.revrange(repo, [opts.pop('rev')])
        patch.export(repo, revs, fp=ui, opts=patch.diffopts(ui, opts))
    else:
        commands.diff(ui, repo, *fnames, **opts)
    content = ui.popbuffer()
    
    if ui.verbose:
        ui.status('Pasting:\n%s\n' % content)
    
    url = pastebins[dest]['handler'](content=content, **opts)
    ui.write('%s\n' % url)


cmdtable = {
    'paste': 
    (paste, [
        ('r', 'rev',   '', 'paste a patch of the given revision(s)'),
        ('d', 'dest',  '', 'the pastebin site to use (defaults to dpaste)'),
        ('t', 'title', '', 'the title of the paste (optional)'),
        ('u', 'user',  '', 'the name of the paste\'s author (defaults to the '
                           'username configured for Mercurial)'),
        ('k', 'keep', False, 'specify that the pastebin should keep the paste for as '
                             'long as possible (optional, not universally supported)'),
    ] + commands.diffopts,
    'hg paste -d PASTEBIN FILE...')
}

help.helptable += (
    (['pastebins', 'pastebins'], ('Pastebins supported by hg-paste'),
     (r'''
    hg-paste only works with dpaste at the moment.  More pastebins will be
    supported in the future.
    
    Available pastebins:
    
    dpaste
        website: http://dpaste.com/
        supported options: --title, --keep, --user
    ''')),
)