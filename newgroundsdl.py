#!/usr/bin/env python3

import urllib.request
import shutil
from bs4 import BeautifulSoup
import sys
import re

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}

if len(sys.argv) != 2:
    print("Usage: newgroundsdl <AUDIO_PAGE_URL>")
    sys.exit(1)

print("Downloading list page...")
req = urllib.request.Request(sys.argv[1], data=None, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read()

soup = BeautifulSoup(html, "html.parser")

wrappers = soup("div", class_="audio-wrapper")
for w in wrappers:
    print("Downloading song page https:" + w.a["href"] + "...")
    req2 = urllib.request.Request("https:" + w.a["href"], data=None, headers=headers)
    with urllib.request.urlopen(req2) as response2, open("debug.html", 'w') as htmout:
        # htmout.write(response2.read().decode("utf-8"))
        soup2 = BeautifulSoup(response2.read(), "html.parser")
        # print(soup2("div", class_="pod"))
        pod = soup2("div", class_="pod")[0] # pod #1 is the audio info
        # print(pod("script")[4])
        metadata = str(pod("script")[4].string) # currently the 8th script in the pod contains the metadata
        fileuri = re.search(r'"url":"([^\?]*)', metadata).group(1) # I could parse json here but I don't feel like it
                                                                # note that it strips off the parameter. I'm not really sure what it's for, but it's definitely not necessary.
        fileuri = re.sub(r'\\(.)', r'\1', fileuri) # unescape the json string
        dlfilename = re.sub(r'.*/', '', fileuri)
        print("Downloading " + dlfilename + "...")
        print(fileuri)
        dlreq = urllib.request.Request(fileuri, data=None, headers=headers)
        with urllib.request.urlopen(dlreq) as dlfile, open(dlfilename, 'wb') as dlout:
            shutil.copyfileobj(dlfile, dlout, length=1024*1024) # block size 1M (the default, 16K, is freakin' slow)
