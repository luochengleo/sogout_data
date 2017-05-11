#coding=utf8
__author__="luocheng"
import htmllib, formatter
from bs4 import BeautifulSoup
import re


def reextract(htmldata, docno, url):
    p1 = re.compile("<.+?\s*href\s*=\s*[\"\']?([^\"\'\s>]+)[\"\']?", re.IGNORECASE)
    htmldata = [item for item in htmldata.split('\n') if len(item) < 1000]
    rtr = []
    for l in htmldata:
        for item in p1.findall(l):
            rtr.append(item)
    return rtr


class AnchorExtractor:
    def __init__(self):
        self.p1 = re.compile("<.+?\s*href\s*=\s*[\"\']?([^\"\'\s>]+)[\"\']?",re.IGNORECASE)

    def extract(self,htmldata, docno,url):
        try:
            parser = htmllib.HTMLParser(formatter.NullFormatter())
            parser.feed(htmldata)
            return parser.anchorlist
        except Exception,ex:
            pass
            return []

    def soupExtract(self,htmldata,docno,url):
        try:
            soup = BeautifulSoup(htmldata,'html.parser')
            anchors = soup.find_all('a')
            links = [a['href'] for a in anchors if a.has_attr('href')]
            return links

        except Exception,ex:
            return []

    def reExtract(self, htmldata, docno, url):
        try:
            rtr = self.p1.findall(htmldata)
            return rtr
        except Exception, ex:
            return []

if __name__=='__main__':
    ae = AnchorExtractor()
