# google-image-downloader

## What's Different from existing github implementations?
The objective of this code is to download `original images`.  
It finds all original sources by clicking all image elements.  
So, it takes long time to download all `original images`.  

## Prerequisites
Python version 3 is used and it tested on Windows10, Mac OS.  
Chrome browser is required.  
```
pip install selenium, wget, urllib
```
You have to feed your chrome browser version into --version argument.  
For example, if your version is 73.0.3683.103 then feed just 73.  
Then, it automatically downloads the chrome driver.
Don't insert space between arguments of --search.  
ex) --search 권나라,` `수지,` `이선빈  
## Usage
```
python google_downloader.py --browser chrome --version 73 --search 권나라,수지,이선빈
```
