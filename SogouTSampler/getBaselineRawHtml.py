# coding=utf8
__author__ = "luocheng"
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from bz2file import BZ2File
from AnchorExtractor import reextract

from DocumentParser import *


if __name__=='__main__':
    tag = sys.argv[1]
    path = '/home/luocheng/zhengyukun/index_build/sogouTSample/sample_result/sogout_data.'+tag+'.comp'
    fout = open('/home/luocheng/dataset/ntcirwww/baseline_html/'+tag,'w')
    import os
    files = os.listdir(path)


    baseline = set()
    for l in open('chn.baseline.trec'):
        baseline.add(l.strip(' ')[2])

    for f in files:
        filepath = path+'/'+f
        dp = DocumentParser(filepath)
        count = 0
        while dp.getWhetherEnd()==False:
            docno, url, content, url = dp.getDocument()
            if docno in baseline:
                fout.write('\n'.join(['<doc>','<docno>'+docno+'</docno>', '<url>'+url+'</url>', content,'</doc>'])+'\n')
    fout.close()


