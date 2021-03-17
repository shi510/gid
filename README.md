# google-image-downloader

## What's Different from existing github implementations?
The objective of this code is to download `original images`.  
It finds all original sources by clicking all image elements.  
So, it takes long time to download all `original images`.  

## Prerequisites
1. Python 3  
2. Crome Browser  
```
pip install selenium, wget, urllib
```
You have to feed your chrome browser version into --version argument.  
For example, if the version is 89.0.4389.90 then feed just 89.  
Then, it automatically downloads the chrome driver.  
Do not insert white-space between arguments comma of --search.  
## Usage
```
python google_downloader.py --version 89 --search "Taylor Swift","Christopher Nolan"
```
