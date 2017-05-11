# coding = utf8
import json

__author__='luocheng'

from  AnchorExtractor import AnchorExtractor
from DocumentParser import DocumentParser
from SampleJudger import SampleJudger
from urlparse import urlparse
from htmlParser import parse_html
from bz2 import BZ2File

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SogouTSampler:
    def __init__(self):
        top1200_threshold = 0.2
        inSerp_threshold = 0.15
        other_threshold = 0.1
        self.cnt_list = [0 for i in range(6)]
        self.sampleJudger = SampleJudger(top1200_threshold, inSerp_threshold, other_threshold)
        self.anchorExtractor = AnchorExtractor()

    def parse(self, dir, filename, platform='win', bz2 = True):
        if platform =='win':
            dp = DocumentParser(dir+'\\'+filename, bz2=bz2)
        elif platform=='unix':
            print '<!--', dir + '/' + filename, '-->'
            dp = DocumentParser(dir + '/' + filename, bz2=bz2)

        # print '<xml version="1.0" encoding="UTF-8"?>'
        # print '\t<urls>'
        output = []

        count = 0
        while dp.getWhetherEnd() == False:

            docno, url, content = dp.getDocument()

            if docno == None:
                continue
            if url.endswith('/'):
                url = url[:-1]
            url = url.lower()

            try:
                try:
                    domain = urlparse(url).netloc
                except:
                    continue

                isKept = self.sampleJudger.sample(url, domain)
                self.cnt_list[isKept] += 1

                if isKept > 0:
                    # print url
                    output.append(json.dumps({'docno': docno, 'url': url, 'type':isKept, 'content': content}))
                    # count += parse_html(content, url, 0)
            except:
                print '<!-- doc exception', url, '-->'

        # print '\t</urls>'
        # print '</xml>'

        output_file = BZ2File('sample/' + dir.split('/')[-1] + '.' + filename[:-3] + 'sample.bz2', 'w')
        output_file.write('\n'.join(output))
        # output_file.write('\n')
        output_file.close()
        return count

    def batchParse(self,dir,startIdx, endIdx):
        from multiprocessing import Process
        import os
        proc_record = []

        files = [item for item in os.listdir(dir) if '.bz2' in item]
        endIdx = min(endIdx,len(files))
        for i in range( endIdx-startIdx):
            p = Process(target = self.parse,args=(dir,files[i+startIdx],))
            p.start()
            proc_record.append(p)
        for p in proc_record:
            p.join()
        for f in os.listdir(dir):
            self.parse(dir,f)


if __name__=='__main__':
    ss = SogouTSampler()
    # la.parse('../rawdata','part-m-00000.bz2',platform='unix',bz2=True)
    dir = sys.argv[1]
    filename = sys.argv[2]
    platform  = sys.argv[3]
    docnum = -1
    import time
    t1 = time.time()
    try:
        docnum = ss.parse(dir, filename, platform=platform)
    except Exception, ex:
        print '<!-- main exception -->'
        pass
    t2 = time.time()
    print '<!-- cnt=', ss.cnt_list, ' -->'
    print '<!-- time=', t2 - t1, 'docnum=', docnum, 'done! -->'



