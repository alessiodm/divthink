def crawl(url):
    tocrawl = set([url])
    crawled = set([])
    depth = random.randint(1, 10)
    response = ""

    while depth > 0:
        try:
            crawling = tocrawl.pop()
            print "Crawling: " + crawling + " - Remains: " + str(depth)
        except KeyError:
            return response
        url = urlparse.urlparse(crawling)
        try:
            response = urllib.urlopen(crawling)
            depth -= 1
        except:
            print "Error opening url: " + crawling
            continue
        msg = response.read()

        # TODO: Get site title
        # TODO: Get site keywords
        links = html.fromstring(msg).xpath('//a')
        crawled.add(crawling)
        #for link in (links.popleft() for _ in xrange(len(links))):
        for link in (links.pop(0) for _ in xrange(len(links))): # Go only for first link...
            if 'href' in link.attrib:
                link = link.attrib['href'] 
            else:
                continue

            if link.startswith('/'):
                link = 'http://' + url[1] + link
            elif link.startswith('#'):
                link = 'http://' + url[1] + url[2] + link
            elif not link.startswith('http'):
                link = 'http://' + url[1] + '/' + link
            if link not in crawled:
                tocrawl.add(link)
    return { 'crawled': list(crawled), 'msg': msg }
    return msg

def get_term(content):
    try:
        tree = html.fromstring(content)  
        paragraphs = tree.xpath('//p')
        if paragraphs:
            for par in paragraphs:
                for word in par.text.split():
                    if len(word) > random.randint(4, 7):
                        return word
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return "_err_term_"

    return "_no_term_"

import sys
from pprint import pprint
from collections import deque
import urllib
import urlparse
import json
import random
from lxml import html

def get_google_results(searchfor):
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    j = json.load(search_response)
    return [url['url'] for url in j['responseData']['results']]

def get_terms(search_content):
    divterms = []
    #try:
    # Get a bunch of keywords
    #search_content = raw_input('Please, insert terms you would like to diverge: ')

    # Search them on google and get links
    urls_to_crawl = get_google_results(search_content)
    #print urls_to_crawl

    # go in depth following links in those pages
    crawled_paths = []
    for url in urls_to_crawl:
        content = crawl(url)
        new_term = get_term(content['msg'])
        crawled_paths.append(content['crawled'])
        # Find some words longer than 4-5 characters
        if new_term not in divterms:
            if new_term not in ['_no_term_', '_err_term_']:
                divterms.append(new_term)

    result = { 'crawled_paths': crawled_paths, 'divterms': divterms}
    return result
    #except Exception, err:
    #    sys.stderr.write('ERROR: %s\n' % str(err))
    #    raise err


    