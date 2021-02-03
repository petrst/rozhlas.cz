# coding: utf-8
import requests
import re
resp = requests.get('https://hledani.rozhlas.cz/iRadio/?query=&reader=&stanice%5B%5D=%C4%8CRo+Vltava&porad%5B%5D=Hra+pro+pam%C4%9Btn%C3%ADky')
all = re.findall('http.*player=on',resp.text)
for hra in all:
    page = requests.get(hra)
    page = page.content.decode('utf-8')
    title = re.search('titulek audia.*?>(.*?)</div>', page).groups()[0]
    title = title.replace(':','-')
    print("Downloading ", title, "...")
    mp3link=re.findall('http.*mp3',page)[0]
    print("from", mp3link)
    print("to", title+'.mp3')
    with open(title+'.mp3', 'wb') as fh:
        r = requests.get(mp3link, stream=True)
        for chunk in r.iter_content(chunk_size=8192):
            fh.write(chunk)
    print("Done")


