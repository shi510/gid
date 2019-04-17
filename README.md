# google-image-downloader

## Prerequisites
Python version 3 is used and it tested on Windows10, Mac OS.  
Chrome browser is required.  
```
pip install selenium, wget, urllib
```
You have to feed your chrome browser version into --version argument.  
For example, if your version is 73.0.3683.103 then feed just 73.  
Then, it automatically downloads chrome driver in current folder.  
Don't insert space in --search arguments.  
ex) --search 권라나,` `수지,` `이선빈  
## Usage
```
python google_downloader.py --browser chrome --verison 73 --search 권나라,수지,이선빈
```
