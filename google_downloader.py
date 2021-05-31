import argparse
import time
import re
import os
import platform
import zipfile
import stat
import ssl

import wget
from tqdm import tqdm
from selenium import webdriver
from urllib.request import urlopen, Request
from urllib.parse import quote

DOWNLOAD_ROOT = 'downloaded_images'

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

    if version == 89:
        root += '89.0.4389.23/'
    elif version == 90:
        root += '90.0.4430.24/'
    elif version == 91:
        root += '91.0.4472.19/'
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

def get_browser(args):
    options = webdriver.ChromeOptions()
    if args.window == 0:
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome('./chromedriver', chrome_options=options)
    return browser

def get_all_image_element_ids(browser, target, more_images=False):
    re_expr_clickable = re.compile('<div.*?jsaction="IE7JUb.+?".*?data-id="(.+?)".*?>')
    search_url = 'https://www.google.com/search?'
    img_url =  search_url + 'q={}&tbm=isch'.format(target)
    browser.get(img_url)
    towards_end_of_scroll(browser)
    if more_images:
        # Click more images
        browser.find_element_by_xpath('//input[@class="mye4qd"]').click()
        towards_end_of_scroll(browser)
    match_results = re_expr_clickable.findall(browser.page_source)
    return match_results

def get_original_image_sources(browser, elem_id):
    re_expr_img_path = re.compile('<img.*?class="n3VNCb".*?src="([http|https].+?)".*?')
    xpath = '//div[@data-id="{}"]'.format(elem_id)
    browser.find_element_by_xpath(xpath).click()
    time.sleep(1)
    html_src = browser.find_elements_by_xpath('//div[@class="v4dQwb"]/a[@class="eHAdSb"]')
    URLs = []
    for src in html_src:
        img_url_html = src.get_attribute('innerHTML')
        results = re_expr_img_path.findall(img_url_html)
        if len(results) > 0:
            URLs.append(results[0])
            if 'encrypted-tbn0' not in results[0]:
                URLs = [results[0]]
                break
    return URLs

def download_url(filename, url, ssl_context):
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
               '(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.3',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'
               }
    try:
        img = urlopen(Request(url=url, headers=headers), context=ssl_context)
        if(not os.path.exists(filename)):
            with open(filename, 'wb') as f:
                f.write(img.read())
    except Exception as e:
        pass

def main(args):
    targets = args.search
    if not exist_chromedriver('./'):
        download_chromedriver(int(args.version))
    browser = get_browser(args)
    for target_name in targets.split(','):
        target_folder = os.path.join(DOWNLOAD_ROOT, target_name)
        os.makedirs(target_folder, exist_ok=True)
        element_ids = get_all_image_element_ids(browser, quote(target_name), args.more_images)
        for e_idx, elem_id in enumerate(tqdm(element_ids)):
            URLs = get_original_image_sources(browser, elem_id)
            if len(URLs) > 0:
                filename = target_folder + '/{}_{}.jpg'
                filename = filename.format(target_name, e_idx+1)
                download_url(filename, URLs[0], ssl_context)

if __name__ == '__main__':
    ssl_context = ssl._create_unverified_context()
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', required=True)
    parser.add_argument('-s', '--search', required=True)
    parser.add_argument('-m', '--more_images', required=False,
        type=bool, default=False)
    parser.add_argument('-w', '--window', type=int,
        default=1, help='show browser (default: 1)')
    args = parser.parse_args()
    main(args)
