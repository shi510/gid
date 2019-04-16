import argparse
from urllib.request import urlopen, Request
from urllib.parse import quote
import re
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", required=True)
    args = parser.parse_args()
    people = args.search

    headers = {'User-Agent': 
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
               '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
               }
    search_url = "https://www.google.com/search?"
    re_expr = re.compile('<img id.+?<div class.+?"ou":"(.+?)".+?:.+?</div>')
    for p in people.split(','):
        pq = quote(p)
        img_url =  search_url + 'q={}&tbm=isch'.format(pq)
        img_req = Request(url=img_url, headers=headers)
        img_html = urlopen(img_req).read().decode('utf-8')
        img_srcs = re_expr.findall(img_html)
        os.mkdir(p)
        for i in enumerate(img_srcs):
            try:
                t = urlopen(Request(url=i[1], headers=headers))
                print(i[1])
                filename = p + '/{}_{}.jpg'.format(p,str(i[0]+1))
                with open(filename,"wb") as f:
                    f.write(t.read())
            except:
                pass
if __name__=="__main__":
    main()