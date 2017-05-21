# coding=utf8
__author__ = "luocheng"
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from bz2file import BZ2File
from AnchorExtractor import reextract

from DocumentParser import *


if __name__=='__main__':
    # tag = sys.argv[1]
    # path = '/home/luocheng/zhengyukun/index_build/sogouTSample/sample_result_xml/sogout_data.'+tag+'.comp'
    # fout = open('/home/luocheng/dataset/ntcirwww/baseline_html/'+tag,'w')
    import os
    path = '../raw'
    fout = open('../output/sogout_data.0.comp.part-m-00000.sample.out', 'w')
    files = os.listdir(path)


    baseline = set()
    for l in open('chn.baseline.trec'):
        baseline.add(l.split(' ')[2])
    baseline.add('002b2ae63faed8b5-cde784dcdebcdc31-4b1d114d1c5754d6836ee824641c746a')

    for f in files:
        filepath = path+'/'+f
        print filepath
        dp = DocumentParser(filepath, bz2=False)

        count = 0
        while dp.getWhetherEnd()==False:
            docno, url, content = dp.getDocument()

            if docno in baseline:
                fout.write('\n'.join(['<doc>','<docno>'+docno+'</docno>', '<url>'+url+'</url>', content,'</doc>'])+'\n')
        print dp.readcount
    fout.close()


