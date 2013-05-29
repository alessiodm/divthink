import sys
from pprint import pprint
from collections import deque
import urllib
import urlparse
import json
import random
from lxml import html

def create_node(name, children):
    return { "name": name, "children": children }

def crawl(addr):
    current = create_node(addr, [])
    root = current
    depth = random.randint(1, 5)
    page_content = ""
    crawled = [] # Not crawl same url twice

    to_crawl = addr
    for i in range(depth):
        remain = depth - i - 1
        print "Crawling: " + to_crawl + " - Remains: " + str(remain)
        url = urlparse.urlparse(to_crawl)
        try:
            response = urllib.urlopen(to_crawl)
        except:
            print "Error opening url: " + to_crawl
            break

        crawled.append(to_crawl)
        page_content = response.read()
        raw_links = html.fromstring(page_content).xpath('//a')
        full_links = []
        
        for link in (raw_links.pop(0) for _ in xrange(len(raw_links))):
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
                full_links.append(link)

        if not full_links: # no link crawlable
            break

        for link in full_links:
            current["children"].append(create_node(link, []))

        rand_link = random.randint(0, len(full_links)) - 1
        print "selected " + str(rand_link + 1) + " of " + str(len(full_links))
        current["children"][rand_link]["visited"] = True
        current = current["children"][rand_link]
        to_crawl = current["name"]

    return { 'crawled': root, 'page_content': page_content }


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

def get_google_results(searchfor):
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    j = json.load(search_response)
    return [url['url'] for url in j['responseData']['results']]

def get_terms(search_content):
    divterms = []
    contents = []
    #try:
    # Get a bunch of keywords
    #search_content = raw_input('Please, insert terms you would like to diverge: ')

    # Search them on google and get links
    urls_to_crawl = get_google_results(search_content)
    #print urls_to_crawl

    # go in depth following links in those pages
    crawled_paths = { "name": search_content, "children": [] }
    for url in urls_to_crawl:
        content = crawl(url)
        #print content['page_content']
        new_term = get_term(content['page_content'])
        crawled_paths["children"].append(content['crawled'])
        # Find some words longer than 4-5 characters
        if new_term not in divterms:
            if new_term not in ['_no_term_', '_err_term_']:
                divterms.append(new_term)

    result = { 'crawled_paths': crawled_paths, 'divterms': divterms }
    return result
    #except Exception, err:
    #    sys.stderr.write('ERROR: %s\n' % str(err))
    #    raise err


