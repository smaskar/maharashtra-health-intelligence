#!/usr/bin/env python3
"""Collect public Marathi/English Google News RSS items into a review queue.
This script intentionally does not auto-publish allegations as verified facts.
"""
from __future__ import annotations
import json, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'review_queue.json'
QUERIES=[
 'NHM Maharashtra OR राष्ट्रीय आरोग्य अभियान महाराष्ट्र',
 'जिल्हा रुग्णालय महाराष्ट्र OR प्राथमिक आरोग्य केंद्र महाराष्ट्र',
 '108 ambulance Maharashtra OR १०८ रुग्णवाहिका महाराष्ट्र',
 'औषध तुटवडा रुग्णालय महाराष्ट्र OR doctor shortage PHC Maharashtra',
 'hospital fire Maharashtra OR रुग्णालय आग महाराष्ट्र',
 'संजय कटकर आरोग्य OR Commissioner Health Services Maharashtra'
]

def fetch(q:str):
    url='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q,'hl':'mr','gl':'IN','ceid':'IN:mr'})
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 NHM-MH-Intelligence/1.0'})
    with urllib.request.urlopen(req,timeout=25) as r: return r.read()

def parse(xml:bytes,q:str):
    root=ET.fromstring(xml); out=[]
    for item in root.findall('.//item')[:30]:
        out.append({'query':q,'title':item.findtext('title',''),'url':item.findtext('link',''),'published':item.findtext('pubDate',''),'source':item.findtext('source',''),'verification':'Unverified Public Collection','status':'Needs Review'})
    return out

def main():
    items=[]
    for q in QUERIES:
        try: items.extend(parse(fetch(q),q))
        except Exception as e: items.append({'query':q,'error':str(e),'status':'Collection Error'})
    seen=set(); dedup=[]
    for x in items:
        key=(x.get('title'),x.get('url'))
        if key not in seen: seen.add(key); dedup.append(x)
    OUT.write_text(json.dumps({'generated_at':datetime.now(timezone.utc).isoformat(),'items':dedup},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'wrote {len(dedup)} items to {OUT}')
if __name__=='__main__': main()
