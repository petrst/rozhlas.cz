#!/usr/bin/python3
# coding: utf-8
import requests
import re
import sys
import os
import eyed3
from io import BytesIO
from PIL import Image

PATH=sys.argv[1]

def get_resized_image(url):
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))
    resize_factor = 600 / img.size[0]
    resized_img = img.resize((int(resize_factor * img.size[0]), int(resize_factor * img.size[1])))
    buf = BytesIO()
    resized_img.save(buf, format='JPEG')
    return buf.getvalue()

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
    filepath = PATH+title+'.mp3'
    print("to", filepath)
    if os.path.isfile(filepath):
        print("Skipping", filepath)
        continue
    with open(filepath, 'wb') as fh:
        r = requests.get(mp3link, stream=True)
        for chunk in r.iter_content(chunk_size=8192):
            fh.write(chunk)
    img_url = re.search('link rel="image_src" href="(.*)"', page).groups()[0]
    print("Image URL", img_url)

    # Fix ID3 tags
    mp3 = eyed3.load(filepath)
    autor, title = title.split('-')
    mp3.tag.artist = autor.strip()
    mp3.tag.title  = title.strip()
    mp3.tag.album  = u"Hra pro pamětníky"
    mp3.tag.images.set(type_=3, img_data=get_resized_image(img_url), mime_type='image/jpg')
    mp3.tag.save(encoding='utf-8')

    print("Done")


