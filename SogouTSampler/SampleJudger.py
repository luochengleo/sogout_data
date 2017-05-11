# coding=utf8
__author__ = 'lucoheng'

from random import random
import sys
import time
'''
定义一个类SampleJudger 来判断是否Sample当前page；
首先把domain分成三个部分，
    A. top 1200
    B. 在queryset的serp上出现的url
    C. 剩下的url

    根据玉昆的统计，这三部分在sogout所有的url占比，大约是各占1/3
    我们目标是通过合理的sample，使得最终得到的结果占到sogout的10~15%

    现在的计划这样的：baike.baidu.com全部保留
    现在的逻辑是这样的：

    input: url
    output: boolean True or False

    url 及相关的domain
    |
    |
    |
    url 是否在queryset的top100 search result page 中------是----> True
    |
    | 否
    |
    domain是否在全保留的域名中------是----> True
    |
    | 否
    |
    |
    domain是否在A------是--------> 以概率p1 返回True， 1-p1 返回False
    |
    | 否
    |
    domain是否在B------是--------> 以概率p2 返回True， 1-p1 返回False
    |
    | 否
    |
    以概率p3 返回True， 1-p3 返回False


'''


class SampleJudger:
    def __init__(self, _p1, _p2, _p3):
        self.keepAll = set()
        self.top1200 = set()
        self.inSerp = set()
        self.top1200_threshold = _p1
        self.inSerp_threshold = _p2
        self.other_threshold = _p3

        #少了一个，如果这个url出现在搜索结果的url集合中，就直接返回true
        # 这个self.inSerp 的区别是，self.inSerp 是出现在Serp中的domain，self.serpUrlSet是url；

        self.serpUrlSet = set()


        for l in open('../data/keepAll.txt'):
            self.keepAll.add(l.strip().lower())

        for l in open('../data/top1200.txt'):
            if l.strip() not in self.keepAll:
                self.top1200.add(l.strip().lower())

        for l in open('../data/inSerp.txt'):
            if l.strip() not in self.keepAll and l.strip() not in self.top1200:
                self.inSerp.add(l.strip().lower())

        for l in open('../data/serpUrls.txt'):
            self.serpUrlSet.add(l.strip().lower())
    '''
    input: url
    output: True or False
    '''
    def sample(self, url, domain):

        if url in self.serpUrlSet:
            return 1

        #domain = self.getDomain(url)
        if domain in self.keepAll:
            return 2
        elif domain in self.top1200:
            rand = random()
            if rand <= self.top1200_threshold:
                return 3
            else:
                return 0
        elif domain in self.inSerp:
            rand = random()
            if rand <= self.inSerp_threshold:
                return 4
            else:
                return 0
        else:
            rand = random()
            if rand <= self.other_threshold:
                return 5
            else:
                return 0

    # '''
    # input: url
    # output: corresponding domain
    # '''
    #
    # def getDomain(self, url):
    #     return ''

if __name__ == '__main__':
    """
    p1 top1200_threshold  = 0.2 33% * 0.2 = 6.6%
    p2 inSerp_threshold = 0.15 33%*0.15 = 4.95%
    p3 other_threshold = 0.1 33%*0.1 = 3.33%

    """
    top1200_threshold = 0.2 # int(sys.argv[1])
    inSerp_threshold = 0.15 # int(sys.argv[2])
    other_threshold = 0.1 # int(sys.argv[3])
    output = open('../data/sample20161123.txt', 'w')
    #output_str = ''
    judger = SampleJudger(top1200_threshold, inSerp_threshold, other_threshold)
    file = open('/home/luocheng/zhengyukun/pagerank_work/hash2url_result/id_url_domain_1103.txt', 'r')
    kept_cnt = 0
    cnt = 0
    cnt_list = [0, 0, 0, 0, 0, 0]
    serpUrl_cnt = 0
    serpDomain_cnt = 0
    KeepAll_cnt = 0
    top1200_cnt = 0
    other_cnt = 0
    for line in file:
        cnt += 1
        if cnt % 10000000 == 0:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt
            # break
        attr = line[:-1].lower().split('\t')
        id = int(attr[0])
        url = attr[1]
        domain = attr[2]
        isKept = judger.sample(url, domain)
        cnt_list[isKept] += 1
        if isKept > 0:
            kept_cnt += 1
            # output_str += str(id) + '\t' + url + '\t' + domain + '\n'
            output.write(str(id) + '\t' + url + '\t' + domain + '\n')

    # output.write(output_str)
    output.close()
    print 'cnt=', cnt, 'kept_cnt=', kept_cnt, sum(cnt_list[1:])
    for i in range(6):
        print cnt_list[i]
