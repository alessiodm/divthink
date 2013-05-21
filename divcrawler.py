import sys
import pprint
import re
import urllib
import urlparse
import json
import random
from lxml import html

def crawl(url):
    tocrawl = set([url])
    crawled = set([])
    #linkregex = re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')
    linkregex = re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')
    #linkregex = re.compile('href=[\'"](.*?)[\'"].*?>')
    #keywordregex = re.compile('<meta\sname=["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')
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
        # Get site title
        """
        startPos = msg.find('<title>')
        if startPos != -1:
            endPos = msg.find('</title>', startPos+7)
            if endPos != -1:
                title = msg[startPos+7:endPos]
                #print title
        """
        # Get site keywords
        """
        keywordlist = keywordregex.findall(msg)
        if len(keywordlist) > 0:
            keywordlist = keywordlist[0]
            keywordlist = keywordlist.split(", ")
            print keywordlist
        """
        links = linkregex.findall(msg)
        crawled.add(crawling)
        for link in (links.pop(0) for _ in xrange(len(links))):
            if link.startswith('/'):
                link = 'http://' + url[1] + link
            elif link.startswith('#'):
                link = 'http://' + url[1] + url[2] + link
            elif not link.startswith('http'):
                link = 'http://' + url[1] + '/' + link
            if link not in crawled:
                tocrawl.add(link)
    return msg

def get_term(content):
    try:
        tree = html.fromstring(content)  
        for word in tree.xpath('//p')[0].text.split():
            if len(word) > 4:
                return word
    except:
        return "ErrorTerm"

    return "NoTerm"


def get_google_results(searchfor):
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    j = json.load(search_response)
    return [url['url'] for url in j['responseData']['results']]

divterms = []

# Get a bunch of keywords
search_content = raw_input('Please, insert terms you would like to diverge: ')

# Search them on google and get links
urls_to_crawl = get_google_results(search_content)
#print urls_to_crawl

# go in depth following links in those pages
for url in urls_to_crawl:
    content = crawl(url)
    # Find some words longer than 4-5 characters
    divterms.append(get_term(content))

print divterms

