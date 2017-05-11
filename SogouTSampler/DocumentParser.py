# coding=utf8
__author__ = "luocheng"
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# encoding:utf-8
from bz2file import BZ2File
from AnchorExtractor import reextract


class DocumentParser:
    def __init__(self, filename, bz2=False):
        if bz2 == False:
            self.reader = open(filename, 'r')
        else:
            self.reader = BZ2File(filename, 'r')
        self.filename = filename
        self.reachEnd = False
        self.readcount = 0

    def getWhetherEnd(self):
        return self.reachEnd

    def getReadCount(self):
        return self.readcount

    def getDocument(self, debug=False):
        docno = None
        url = None
        content = []
        if self.getWhetherEnd():
            return None, None, None
        else:
            status = 0
            while True:
                if debug:
                    pass

                s = self.reader.readline()
                self.readcount += 1
                if len(s) == 0:
                    self.reachEnd = True
                    return None, None, None
                else:
                    if status == 0:
                        if s.strip() == '<doc>':
                            status = 1
                        else:
                            pass
                    elif status == 1:
                        docno = s
                        status = 2
                    elif status == 2:
                        url = s
                        status = 3
                    elif status == 3:
                        if s.strip() == '</doc>':
                            docno = docno[7:len(docno) - 10]
                            url = url[5:len(url) - 8]
                            content_s = ''.join(content)
                            return docno, url, content_s
                        else:
                            content.append(s)


if __name__ == '__main__':
    dp = DocumentParser('../rawdata/part-m-00000')
    count = 0

    while dp.getWhetherEnd() == False:
        count += 1
        docno, url, content = dp.getDocument()
        lt = reextract(content, docno, url)
