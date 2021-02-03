# coding: utf-8
import requests
import re
import eyed3

resp = requests.get('https://hledani.rozhlas.cz/iRadio/?query=&reader=&stanice%5B%5D=%C4%8CRo+Dvojka&porad%5B%5D=Hra+na+ned%C4%9Bli')
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

    # Fix ID3 tags
    mp3 = eyed3.load(filepath)
    autor, title = title.split('-')
    mp3.tag.artist = autor.strip()
    mp3.tag.title  = title.strip()
    mp3.tag.album  = u"Hra na neděli"
    mp3.tag.save(encoding='utf-8')

    print("Done")
