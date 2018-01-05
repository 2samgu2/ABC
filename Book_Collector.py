# -*- coding: utf-8 -*-
import urllib
import urllib2
import lxml
import xml.etree.ElementTree as ET
import bs4
import tool.regex as re
import time
import tool.retry as rt

@rt.retry(Exception, tries=4, delay=10, backoff=1)
def url_req(url, opts=[]):
    req = urllib2.Request(url)
    for opt in opts:
        req.add_header(opt.keys()[0], opt.values()[0])
    r = urllib2.urlopen(req)
    txt = r.read()
    r.close()
    return txt

def getCat(result, pattern, node_dir):
    cat = []
    if pattern:
        m = re.search(pattern, result, re.DOTALL)
        if (m):
            found = m.group(0)
        else:
            return False
    else:
        found = result
    t = ET.fromstring(found)
    return t.findall(node_dir)[0].text

def get_keyword(isbn):
    encText = urllib.urlencode(
        {'key': '84099c30c7b6bacd96e315e8c8d90820', 'detailSearch': 'true', 'isbnOp': 'isbn', 'isbnCode': isbn,
         'category': 'dan'})
    url = "http://www.nl.go.kr/app/nl/search/openApi/search.jsp?" + encText
    result = url_req(url)
    pattern = ''
    node_dir = './result/item/id'
    try:
        book_id = getCat(result, pattern, node_dir).strip()
        encText = urllib.urlencode({'searchmode': 'MarcViewAction', 'vdkvgwkey': book_id})
        url = "http://www.nl.go.kr/nl/search/SearchKolis.nl?" + encText
    except IndexError:
        pass

    result = url_req(url)
    html = bs4.BeautifulSoup(result, "lxml")
    ps = html.findAll('td')
    for idx, p in enumerate(ps):
        if p.text == '653':
            return ps[idx + 2].text
    return None

class Object(object):
    pass

def getISBN(result):
    html = bs4.BeautifulSoup(result, "lxml")
    book_list = html.findAll("div", class_="searchList")
    book_arr = []
    if len(book_list) == 0:
        return False
    for book in book_list:
        cbx = book.find("input", {"name": "cbx"}).get('value')
        isbn = cbx.split("%7C%7CMA%7C%7C")[0].rsplit("%7C%7C",1)[1]
        if isbn != "":
            subject = book.find("input", {"name": "cbx"}).get('title')
            obj = Object()
            obj.subject = subject
            obj.isbn = isbn
            book_arr.append(obj)
    return book_arr

def iskeywordexist(isbn):
    if(get_keyword(isbn) != None):
        return True
    else:
        return False

class Book_Collector:
    def __init__(self):
        self.url = "http://www.nl.go.kr/nl/search/search.jsp?" \
                   "topF1=title&category=dan&all=on&" \
                   "detailSearch=true&sort=iregdate&desc=desc&kdcddc=kdc&kdcddcCode="

    def make_collection(self,filename, category):
        i = 1
        while True:
            full_url = self.url + str(category) + "&" + "pageNum=" + str(i) + "&pageSize=100"
            result = url_req(full_url)
            books = getISBN(result)
            if books is not False:
                for book in books:
                    if '+' in book.isbn:
                        book.isbn = book.isbn.split('+')[0]
                    if '_' not in book.isbn and iskeywordexist(book.isbn):
                        #row = urldecode(book.subject).encode('utf-8') + urldecode("!#@!#@" + str(book.isbn) + "\n").encode('utf-8')
                        row = u'!#@!#@'.join((book.subject, book.isbn)).encode('utf-8').strip()
                        row = str(row) + '\n'.encode('utf-8')
                        print row
                        with open(filename + ".txt", 'a') as f:
                            f.write(row)
                print str(100*i) +" items done"
            else:
                break

            print "scanned " + str(i) + "th page, count :" + str(len(books))

            i += 1
            time.sleep(1)

if __name__ == '__main__':
    """
        philosophy : 1
        religion : 2
        social_science : 3
        natural_science : 4
        descriptive_science : 5
        art : 6
        linguistic : 7
        literature : 8
        history : 9
    """
    c = Book_Collector()
    start_time = time.time()
    print "philosophy start"
    c.make_collection('1_philosophy', 1)
    print("--- %s seconds ---" % (time.time() - start_time))