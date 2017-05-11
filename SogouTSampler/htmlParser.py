# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
import os
from xml.sax.saxutils import escape

def generate_index():
    pass

def add_file(root_dir):
    web_count = 0

    # global f
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if os.path.isdir(path):
            add_file(path)
        else:
            filename = os.path.basename(path)
            if filename != ".DS_Store":
                # f.write(path[7:] + ' ' + str(web_count) + '\n')
                web_count += 1


def my_escape(data):
    """Escape &, <, and > in a string of data.

    You can escape other strings of data by passing a dictionary as
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.
    """

    # must do ampersand first
    data = data.replace("&", "&amp;")
    data = data.replace(">", "&gt;")
    data = data.replace("<", "&lt;")
    data = data.replace("\"", "&quot;")
    return data

def process_content(s):
    s = ' '.join(s.split())
    s = ''.join(s.split('\''))
    s = ''.join(s.split('\"'))
    s = ''.join(s.split('\n'))
    for i in range(33):
        s = ''.join(s.split(chr(i)))
    s = my_escape(s)
    return s


# def gen_graph(filename, index, index_dict, f):
#     if (os.path.isfile(filename)):
#         soup = BeautifulSoup(open(filename), 'lxml')
#         if soup.title:
#             # print soup.title.text
#             title = process_content(soup.title.text)
#             # 处理超链接， 获取锚文本
#             anchor_list = []
#             # 生成链接
#             link_list = []
#             for a in soup.find_all('a'):
#                 if 'href' in a.attrs and a.string:
#                     href = a.attrs['href'][7:]
#                     if href[0:7] == 'http://':
#                         href = href[7:]
#                     # print href, a.string
#                     # 锚文本
#                     anchor_list.append(a.string)
#                     if href in index_dict:
#                         link_list.append(index_dict[href])
#
#                     else:
#                         if href + 'index.html' in index_dict:
#                             link_list.append(index_dict[href + 'index.html'])
#             if len(link_list) > 0:
#                 f.write(index + ':' + ','.join(link_list) + '\n')
#         return


def parse_html(content, url, pr):
    try:
        soup = BeautifulSoup(content, 'html.parser')
    except:
        print '<!-- no html parser', url, '-->'
        try:
            soup = BeautifulSoup(content, 'lxml')
        except:
            print '<!-- no lxml parser', url, '-->'
            return 0

    if soup.title:
        title = process_content(soup.title.text)
        # 处理超链接， 获取锚文本
        anchor_list = []
        content_list = []
        # 生成链接
        tmp_list = soup.find_all('a')
        for a in tmp_list:
            if 'href' in a.attrs and a.string:
                # 锚文本
                anchor_list.append(a.string)
            elif a.string:
                content_list.append(a.string)

        anchor = ' '.join([process_content(k) for k in anchor_list])
        # 处理h1-h6
        h = [0]
        for i in range(1, 7):
            h1_list = []
            tmp_list = soup.find_all('h' + str(i))
            for h1 in tmp_list:
                if h1.string:
                    h1_list.append(h1.string)
            h1 = ' '.join([process_content(k) for k in h1_list])
            h.append(h1)
        # 处理strong
        strong_list = []
        tmp_list = soup.find_all('strong')
        for strong in tmp_list:
            if strong.string:
                strong_list.append(strong.string)
        strong = ' '.join([process_content(k) for k in strong_list])
        # 处理页面内容

        tmp_list = soup.find_all(['p', 'font'])
        for p in tmp_list:
            if p.string:
                content_list.append(p.string)
        p = ' '.join([process_content(k) for k in content_list])

        # 输出xml
        print '\t\t<doc title=\"' + title + '\" url=\"' + my_escape(url) + '\" pr=\"' + str(pr) + '\"'
        # print '\t\t\tdocContent=\"' + docContent + '\"'

        len_split = 10000
        for i in range(int(len(p)/len_split)):
            print '\t\t\tdocContent'+str(i)+'=\"' + p[i*len_split:(i+1)*len_split] + '\"'
        print '\t\t\tdocContent=\"' + p[len_split * int((len(p))/len_split):] + '\"'

        for i in range(int(len(anchor)/len_split)):
            print '\t\t\tanchor'+str(i)+'=\"' + anchor[i*len_split:(i+1)*len_split] + '\"'
        print '\t\t\tanchor=\"' + anchor[len_split * int((len(anchor))/len_split):] + '\"'

        for i in range(1, 7):
            print '\t\t\th' + str(i) + '=\"' + str(h[i]) + '\"'
        print '\t\t\tstrong=\"' + strong + '\"'
        print '\t\t/>'

    return 1


# if __name__ == '__main__':
#
#     filter_suffix = ['doc', 'pdf', 'jsp', 'php', 'asp', 'aspx', 'docx', 'txt']
#     f = open('node_id')
#     file_dict = {}
#     index_dict = {}
#     # 只会parse一些html，在计算锚文本的时候仍然会考虑doc等文件
#     for line in f:
#         linearr = line.strip().split()
#         if len(linearr) > 1:
#             index = linearr[-1]
#             if not index.isdigit():
#                 continue
#             filename = ''
#             for l in linearr[:-1]:
#                 filename += l
#             file_dict[index] = filename
#             index_dict[filename] = index
#
#     # print '<xml>'
#     # print '\t<urls>'
#     # f2 = open('graph', 'w')
#     fpr = open('graph_result')
#     pr = {}
#     for line in fpr:
#         linearr = line.strip().split()
#         pr[linearr[0]] = linearr[1]
#
#     count = 0
#     perc = len(file_dict.keys()) / 1000 + 1
#     for index in file_dict.keys():
#         # if count%perc == 0:
#         # 	print count/perc
#         # count += 1
#         filename = file_dict[index]
#         temp = filename.split('.')
#         if temp[-1] == 'html':
#             if index not in pr:
#                 pr[index] = 0
#             #parse_html('mirror/' + filename, index, index_dict, pr[index])
#     # print '\t</urls>'
#     # print '</xml>'
# # parse_html('mirror/academic.tsinghua.edu.cn/index.html', str(1), index_dict, 0)
