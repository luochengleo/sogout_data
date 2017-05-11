# coding: utf-8

from bz2file import BZ2File
import json
from id_tree import *
import sys
import linecache
from io import StringIO

reload(sys)
sys.setdefaultencoding('utf-8')


def get_url_html(tree, doc_id):
    path_info = id2path(doc_id, tree)
    if path_info != 'wrong id':
        path = '/home/luocheng/zhengyukun/index_build/sogouTSample/sample_result/sogout_data.' + path_info[0] + \
               '.comp/sogout_data.' + path_info[0] + '.comp.part-m-' + path_info[1] + '.sample.bz2'
        f = BZ2File(path, 'r')
        # print 'begin'
        # f.read()
        # print 'end'
        cnt = 0
        for line in f:
            cnt += 1
            if cnt == path_info[2]:
                try:
                    return json.loads(line)
                except:
                    return 'wrong id'
        f.close()
        # try:
        # line = linecache.getline(path, path_info[2])
        # if url_flag == True:
        # return json.loads(line)['url']
        # else:
        # return json.loads(line)['content']
        # except:
        # return 'wrong id'
    return 'wrong id'


tree = build_tree()

f_in = open('chn.baseline.trec', 'r')
# f_in = open('test', 'r')
lines = f_in.readlines()
f_in.close()

f_out = open('html_res.txt', 'a')

cnt = 0
for line in lines:
    cnt += 1
    line = line.strip('\n')
    element_list = line.split()
    doc_id = element_list[2]
    html_url_dict = get_url_html(tree, doc_id)
    html = 'wrong id'
    url = 'wrong id'
    if html_url_dict != 'wrong id':
        html = html_url_dict["content"]
        url = html_url_dict["url"]
    f_out.write('<doc>\n')
    f_out.write('<docno>' + doc_id + '</docno>\n')
    f_out.write('<url>' + url + '</url>\n')
    f_out.write(html)
    f_out.write('</doc>\n\n')
    print str(float(cnt) / 99282 * 100) + '%'
f_out.close()
