from selenium import webdriver
from urllib.request import urlopen, Request
from urllib.parse import quote
import argparse
import time
import re
import os
import platform
import wget
import zipfile
import stat

def towards_end_of_scroll(browser):
    len_script = 'window.scrollTo(0, document.body.scrollHeight);'\
                 'var lenOfPage=document.body.scrollHeight;return lenOfPage;'

    lenOfPage = browser.execute_script(len_script)
    match=False
    while match==False:
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script(len_script)
        if lastCount==lenOfPage:
            match=True

def download_chromedriver(version):
    root = 'https://chromedriver.storage.googleapis.com/'
    os_name = platform.system()

    if version == 74:
        root += '74.0.3729.6/'
    elif version == 73:
        root += '73.0.3683.68/'
    elif version == 72:
        root += '72.0.3626.69/'
    else:
        raise 'Wrong chrome version : ' + version

    if os_name == 'Windows':
        root += 'chromedriver_win32.zip'
    elif os_name == 'Linux':
        root += 'chromedriver_linux64.zip'
    elif os_name == 'Darwin':
        root += 'chromedriver_mac64.zip'
    else:
        raise 'Wrong OS name : ' + os_name

    driver_name = wget.download(root)
    with zipfile.ZipFile(driver_name, 'r') as z:
        z.extractall('.')
    if os_name == 'Linux' or os_name == 'Darwin':
        os.chmod('chromedriver', stat.S_IXUSR)

def exist_chromedriver(path):
    for f in os.listdir(path):
        if 'chromedriver' in f:
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--browser', required=True)
    parser.add_argument('-v', '--version', required=True)
    parser.add_argument("-s", "--search", required=True)
    args = parser.parse_args()
    targets = args.search
    if not exist_chromedriver('./'):
        download_chromedriver(int(args.version))
    browser = webdriver.Chrome('./chromedriver')
    headers = {'User-Agent': 
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
               '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
               }

    search_url = "https://www.google.com/search?"
    re_expr = re.compile('<img id="(.+?)".+?<div class.+?'\
                         '"ou":"(.+?)".+?:.+?</div>')
    for t in targets.split(','):
        quoted = quote(t)
        img_url =  search_url + 'q={}&tbm=isch'.format(quoted)
        browser.get(img_url)
        towards_end_of_scroll(browser)
        browser.find_element_by_xpath('//input[@class="ksb"]').click()
        towards_end_of_scroll(browser)
        img_srcs = re_expr.findall(browser.page_source)

        if(not os.path.exists(t)):
            os.mkdir(t)
        for n, pair in enumerate(img_srcs):
            img_id = pair[0]
            img_src = pair[1]
            try:
                img = urlopen(Request(url=img_src, headers=headers))
                img_id = img_id.split(':')[0]
                filename = t + '/{}_{}.jpg'.format(n+1, img_id)
                if(not os.path.exists(filename)):
                    print('download : ' + img_src)
                    with open(filename,"wb") as f:
                        f.write(img.read())
            except:
                print('can not access : {}'.format(img_src))
if __name__=="__main__":
    main()