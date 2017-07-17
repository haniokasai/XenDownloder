# coding: UTF-8
import os
import cfscrape
import re

if not os.path.exists("download"):
 os.mkdir("download")
scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
print scraper.get("https://forum.pmmp.jp/attachments/1380/").content

#https://torina.top/detail/161/
i=0

while(True):
    try:
        i = i + 1
        res = scraper.get("https://forum.pmmp.jp/attachments/" + str(i) + "/", stream=True)
        fname = re.findall("filename=(.+)", res.headers['content-disposition'])
        parsedfname = fname[0].replace("\"", "")
        #phar名編集
        r = re.compile("(.*).phar(.*)")
        m = re.search(parsedfname,"(.*)(.*)")
        parsedfname =  re.sub(r'[\\|/|:|?|.|"|<|>|\|]',"",parsedfname.split('.phar')[0].split(";")[0])[0:25]+".phar"
        print parsedfname
        f = open('log.txt', 'a')  # 書き込みモードで開く
        f.write(parsedfname+" : "+"https://forum.pmmp.jp/attachments/" + str(i) + "/")  # 引数の文字列をファイルに書き込む
        f.write('\n')
        f.close()  # ファイルを閉じる
        if res.status_code == 200:
            with open("download/"+parsedfname, 'wb') as file:
                for chunk in res.iter_content(chunk_size=10240000):
                    file.write(chunk)
    except KeyError:
        print "NotFound : https://forum.pmmp.jp/attachments/"+str(i)
        f = open('log.txt', 'a')  # 書き込みモードで開く
        f.write("NotFound : https://forum.pmmp.jp/attachments/"+str(i))  # 引数の文字列をファイルに書き込む
        f.write('\n')
        f.close()  # ファイルを閉じる

    print