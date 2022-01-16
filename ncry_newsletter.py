#!/usr/bin/env python3

import os
import os.path
import re
import requests

import urllib.request
from bs4 import BeautifulSoup

def destination_dir():
    home = os.environ['HOME']
    dest = os.path.join(home,'Documents/NCRY_Newsletter')

    if os.path.isdir(dest):
        return dest
    else:
        raise Exception("%s is not a directory" % (dest))

def download(dest, newsletter_urls):
    for url in newsletter_urls:
        filename = re.sub(r'.*[/]', '', url)
        fqpn = os.path.join(dest, filename)

        if not os.path.isfile(fqpn):
            print("need to download", fqpn)
            urllib.request.urlretrieve(url, fqpn)

def main():
    dest = destination_dir()
    print("NCRY downloader into %s" % (dest))

    req = requests.get('https://www.ncry.org/about/newsletter/')
    soup = BeautifulSoup(req.text, 'html.parser')
     
    newsletter_urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            regex_result = re.search(r'NCRy_ClubCar', href)
            if regex_result is not None:
                newsletter_urls.append(href)

    download(dest,newsletter_urls)

if __name__ == "__main__":
    main()
    print("Exiting cleanly")
