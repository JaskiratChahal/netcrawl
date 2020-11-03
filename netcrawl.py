""" Implement a very simple web crawler. It should accept a single
 starting URL, such as https://news.ycombinator.com, as its input.
 It should download the web page available at the input URL and
 extract the URLs of other pages linked to from the HTML source code.
 Although there are several types of link in HTML, just looking at the href
 attribute of tags will be sufficient for this task. It should then attempt to
 download each of those URLs in turn to find even more URLs, and then download
 those, and so on. The program should stop after it has discovered 100 unique
 URLs and print them (one URL per line) as its output.
"""

""" Author: Jaskirat Chahal
Date last modified: 03 November 2020
This program recursively returns a set of urls, from a given starting url.
"""
import requests
from bs4 import BeautifulSoup
from urllib.request import urlparse
from collections import deque

visited_urls = deque()
domains = set()
setOfUrls = set()

def print_urls():
    """Print each URL on a new line."""
    for url in setOfUrls:
        print(url)
    print(f"\n{len(setOfUrls)} unique urls returned.")

def is_valid(parsed):
    """Check if the parsed URL is a valid URL"""
    return bool(parsed.netloc) and bool(parsed.scheme)

def is_unique(href):
    """Check if URL contains a unique domain."""
    cleaned_url = urlparse(href).netloc
    for domain in domains:
        if domain == cleaned_url:
            return False
    return True

def scrape(url, n):
    """Recursively find unique URLs given a starting URL."""
    # attempt to visit url
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception:
        return

    # download all the html content on the webpage
    source = response.content

    # parse the source
    html = BeautifulSoup(source, "html.parser")

    # find all the <a> tags
    tags = html.find_all('a')

    # iterate through all <a> tags
    for tag in tags:

        # retrieve the href value
        href = tag.get("href")

        # parse the href value
        parsed_href = urlparse(href)

        # skip email addresses
        if parsed_href.scheme == "mailto":
            continue

        # skip non-valid urls
        if not is_valid(parsed_href):
            continue

        # clean and join URL
        cleaned_url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        # add cleaned url to visited urls deque
        visited_urls.append(cleaned_url)

        # skip non-unique urls
        if not is_unique(cleaned_url):
            continue

        # add cleaned_url to unique URL set
        setOfUrls.add(cleaned_url)

        # add domain to set of visited domains
        domains.add(urlparse(cleaned_url).netloc)

        # if limit reached, return
        if len(setOfUrls) >= n:
            return

    # recursive call
    while len(setOfUrls) < n and len(visited_urls) > 0:
        scrape(visited_urls.popleft(), n)


if __name__ == "__main__":

    starting_url = "https://news.ycombinator.com"
    scrape(starting_url, 100)
    print_urls()
