# -*- coding: utf-8 -*-
#VERSION: 1.00
#AUTHORS: Anatoly Mayorov (mmajor@yandex.ru)
# This plugin is licensed under the GNU GPL Version 2.

from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
from urllib import quote
import re


torrent_pattern = re.compile(r'''<tr class=".*"><td>.*</td><td.*><a class="downgif" href="(?P<link>.+)"><img src=".+" alt="D" /></a><a href=".+"><img src=".+" alt="M" /></a>\s*<a href=".*">(?P<name>.+)</a></td>\s*(<td align="right">.+<img.*></td>)?\s*<td align="right">(?P<size>.+)</td><td align="center"><span class="green"><img src=".+" alt="S" />(?P<seeds>.*)</span> <img src=".*" alt="L" /><span class="red">(?P<leech>.+)</span></td></tr>''')

tag = re.compile(r'<.*?>')


class rutor(object):
    
    ''' RUTOR.ORG Russian free tracker '''

    url = 'http://rutor.org'

    name = 'rutor.org'

    supported_categories = {'all': 0,
                            'movies': 1,
                            'tv': 6,
                            'music': 2,
                            'games': 8,
                            'anime': 10,
                            'software': 9,
                            'pictures': 3,
                            'books': 11}

    query_pattern = '%(url)s/search/%(start)i/%(f)i/000/2/%(q)s'

    def __init__(self):
        pass

    def search_page(self, what, cat, start):
        params = {'url': self.url,
                'q': quote(what),
                'f': self.supported_categories[cat],
                'start': start}
        dat = retrieve_url(self.query_pattern % params)
        for el in torrent_pattern.finditer(dat):
            d = el.groupdict()
            d['link'] = d['link']
            d['engine_url'] = self.url
            d['name'] = tag.sub('', d['name'])
            yield d

    def search(self, what, cat='all'):
        start = 0
        f = True
        while f:
            f = False
            for d in self.search_page(what, cat, start):
                prettyPrinter(d)
                f = True
            start += 1
