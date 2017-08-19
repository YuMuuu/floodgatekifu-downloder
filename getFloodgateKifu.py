
# coding: utf-8

# In[22]:

import datetime
import pandas as pd
import urllib.request
from time import sleep
import os
import zipfile

from time import sleep
CONNECTION_RETRY = 10

url1 = 'https://floodgate.shogidb2.com/archives/'
url2 = '.zip'



def set_date():
    today = datetime.date.today()
    first_day = datetime.date(2015, 11, 1)
    #first_day = datetime.date(2015, 12, 13)
    
    global date_list
    date_list = pd.date_range(first_day,today -  datetime.timedelta(days=1)).strftime('%Y%m%d')
    print('{0}日分の棋譜をダウンロードします'.format(date_list.size))

def creat_link():
    print('ダウンロード先: ' + os.path.abspath("."))
    for date in date_list:
        file_url = url1 + date + url2
        print ('ダウンロード元: ' + file_url)
        url = file_url
        title = date + url2
        download(url, title)
        print('ダウンロード中')
        sleep(1)
    print('全てのファイルのダウンロードが完了しました')
    
    
def download(url, title):
        for i in range(1, CONNECTION_RETRY + 1):
            try:
                urllib.request.urlretrieve(url,"{0}".format(title))
                urllib.request.urlcleanup()
            except urllib.error.URLError as e:
                print("error:{e} retry:{i}/{max}".format(e=e.reason, i=i, max=CONNECTION_RETRY))
                sleep(i * 5)
            else:
                return True
        return False

def make_dir():
    dir_name = 'floodgate_kifu'
    if os.path.isdir(dir_name):
        print(dir_name + 'が既に存在します。当該ファイル上に展開します')
    else:
        print(dir_name + 'を作成します。')
        os.makedirs(dir_name)
    
def open_zip():
    print('zipファイルを展開します')
    for date in date_list:
        title = date + url2
        try:
            with zipfile.ZipFile(title, 'r') as zf:
                zf.extractall('floodgate_kifu')
        except Exception as e:
                print("error:{e} ".format(e=e))                    
    print('展開が完了しました') 
    
def rm_zip():
    print('zipファイルを削除します')
    for date in date_list:
        title = date + url2
        try:
            os.remove(title)
        except Exception as e:
            print("error:{e} ".format(e=e))      
    print("zipファイルを削除しました")
    
    
if __name__ == '__main__':
    print('floodgateの棋譜をダウンロードします')
    set_date()
    creat_link()
    make_dir()
    open_zip()
    rm_zip()


# In[ ]:



