# -*- coding: utf-8 -*-
"""動作確認用のデモGPXを作る。

実在の大会のGPXは主催者の配布物なのでリポジトリに入れない。
代わりに OSRM の公開デモサーバで実道路に沿ったルートを引き、
架空のPCを打ったGPXを app/samples/demo.gpx に書き出す。

    py tools/make_sample.py [取得済みのOSRM応答.json]
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'app', 'samples', 'demo.gpx')

# 札幌駅 → 北広島 → 千歳 → 苫小牧（実道路。約75km）
VIA = [(141.3508, 43.0686), (141.5630, 42.9855), (141.6510, 42.8210), (141.6050, 42.6340)]
url = 'https://router.project-osrm.org/route/v1/driving/' + ';'.join(f'{lon},{lat}' for lon, lat in VIA) \
      + '?overview=full&geometries=geojson'
import sys
if len(sys.argv) > 1:              # 取得済みのJSONを渡せる（SSL検証が通らないネットワーク用）
    data = json.load(open(sys.argv[1], encoding='utf-8'))
else:
    with urllib.request.urlopen(url, timeout=60) as r:
        data = json.load(r)
coords = data['routes'][0]['geometry']['coordinates']
dist_km = data['routes'][0]['distance'] / 1000
print(f'{len(coords)} 点, {dist_km:.1f} km')

# 架空のPC：ルート上の点をそのまま使う（名前はデモ）
n = len(coords)
wpts = [
    ('START　デモ駅前', coords[0]),
    ('PC1　デモマート北広島店', coords[int(n * 0.3)]),
    ('通過チェック　デモ公園', coords[int(n * 0.55)]),
    ('PC2　デモストア千歳店', coords[int(n * 0.72)]),
    ('FINISH　デモ港', coords[-1]),
]
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gpx version="1.1" creator="Eat on GPX demo" xmlns="http://www.topografix.com/GPX/1/1">',
         '  <metadata><name>デモBRM 札幌→苫小牧</name></metadata>']
for name, (lon, lat) in wpts:
    lines.append(f'  <wpt lat="{lat:.6f}" lon="{lon:.6f}"><name>{name}</name></wpt>')
lines.append('  <trk><name>デモBRM 札幌→苫小牧</name><trkseg>')
for lon, lat in coords:
    lines.append(f'    <trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
lines.append('  </trkseg></trk>')
lines.append('</gpx>')
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')
print('wrote', os.path.normpath(OUT))
