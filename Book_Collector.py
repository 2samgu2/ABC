# -*- coding: utf-8 -*-
import urllib2
import bs4
import urllib
import time

import sys


def urldecode(s):
    return urllib.unquote_plus(s).decode('utf8')


def url_req(url):
    req = urllib2.Request(url)
    result = ""
    try:
        r = urllib2.urlopen(req)
        result = r.read()
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print str(e.args[0]).decode('cp949','ignore') + str(e.args[1]).decode('cp949','ignore')
    return result


class Book_Collector:
    def __init__(self):
        self.url = "http://www.nl.go.kr/nl/search/search.jsp?" \
                   "topF1=title&category=dan&all=on&" \
                   "detailSearch=true&sort=iregdate&desc=desc&kdcddc=kdc&kdcddcCode="

    def getISBN(result, count):
        html = bs4.BeautifulSoup(result, "lxml")
        book_list = html.findAll("div", class_="searchList")
        book_arr = []
        if len(book_list) == 0:
            return False, count
        for book in book_list:
            cbx = book.find("input", {"name": "cbx"}).get('value')
            isbn = cbx.split("%7C%7CMA%7C%7C")[0].rsplit("%7C%7C",1)[1]
            if isbn != "":
                subject = cbx.split("%7C%7C%7C%7C")[1].split("%7C%7C%7C%7C%7C%7C")[0]
                book_arr.append([subject, isbn])
                count += 1

        return book_arr, count

    def make_collection(self,filename, category):
        f = open(filename+".txt", 'w')
        count = 0
        i = 1
        while True:
            full_url = self.url + str(category) + "&" + "pageNum=" + str(i) + "&pageSize=100"
            result = url_req(full_url)
            book_arr, count = self.getISBN(result, count)
            if count > 10000:
                print "scanned " + str(i) + " pages, count :" + str(count)
                break
            elif book_arr is not False:
                for book in book_arr:
                    row = urldecode(book[0]).encode('utf-8') + urldecode("!#@!#@" + str(book[1]) + "\n").encode('utf-8')
                    f.write(row)
            else:
                break

            # print "scanned " + str(i) + "th page, count :" + str(count)

            i += 1
            time.sleep(1)

        f.close()


if __name__ == '__main__':
    """
        철학 : 1
        종교 : 2
        사회과학 : 3
        자연과학 : 4
        기술과학 : 5
        예술 : 6
        언어 : 7
        문학 : 8
        역사 : 9
    """
    c = Book_Collector()
    start_time = time.time()
    print "철학 시작"
    c.make_collection('1_philosophy', 1)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "종교 시작"
    c.make_collection('2_religion', 2)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "사회과학 시작"
    c.make_collection('3_social_science', 3)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "자연과학 시작"
    c.make_collection('4_natural_science', 4)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "기술과학 시작"
    c.make_collection('5_descriptive_science', 5)
    print("--- %s seconds ---" % (time.time() - start_time))
    print sys.stdin.encoding
    print "예술 시작"
    c.make_collection('6_art', 6)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "언어 시작"
    c.make_collection('7_linguistic', 7)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "문학 시작"
    c.make_collection('8_literature', 8)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "역사 시작"
    c.make_collection('9_history', 9)
    print("--- %s seconds ---" % (time.time() - start_time))
    print "완료"
