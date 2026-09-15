# Eat on GPX

GPXファイルを読み込んで、ルート沿いのコンビニ・レストラン・ファストフード・カフェ・日帰り温泉を
地図とリスト（スタートからの距離順）で表示するWebアプリです。
各スポットは「地図↗」からGoogleマップ（iPhoneならアプリ）で開けます。

- 紹介ページ: <https://pikaring.github.io/eat-on-gpx/>
- ツール本体: <https://pikaring.github.io/eat-on-gpx/app/>

## 構成

- `index.html` … 紹介ページ（`assets/` に配色・アイコン・OGP画像）
- `app/index.html` … ツール本体（単一HTML。ビルド不要）
- `app/samples/` … 動作確認用のGPX
- `make_icon.py` / `make_og.py` … アイコンとOGP画像の生成（PIL。外部素材は使わない）

## 使い方

1. `app/index.html` を開く（ローカルファイルでも、Webサーバに置いても可）
2. GPXファイルをドロップするか「GPXを開く」で選ぶ
3. 自動で検索が走り、地図にマーカー、右（スマホでは下）に距離順リストが出る
4. 上部のチップで種類の表示／非表示、「GPX書き出し」で表示中のスポットをウェイポイントとして保存（サイコン等に取り込める）

URLに `?gpx=samples/xxx.gpx` を付けると起動時に読み込みます。

## 地図とデータの2モード

| | 地図 | スポットの取得元 | 必要なもの |
|---|---|---|---|
| Googleモード | Google Maps | Google Places API (New) | APIキー |
| OSMモード（既定） | OpenStreetMap（Leaflet） | Overpass API | なし |

設定（⚙）にAPIキーを入れるとGoogleモードになります。取得元だけOSMにすることも可能です。

### Google APIキーの準備

1. [Google Cloud Console](https://console.cloud.google.com/google/maps-apis/credentials) でプロジェクトを作り、請求先を設定
2. 「Maps JavaScript API」と「Places API (New)」を有効化
3. APIキーを作成し、アプリケーションの制限を「HTTPリファラー」にして公開URLを登録（ローカルで開くだけなら制限なしでも可）
4. 設定ダイアログに貼り付けて保存（ブラウザの localStorage にのみ保存されます）

費用の目安：Places Nearby Search は 200 km のルートで「ルートからの距離 300 m」なら約250回。
無料枠に収まる範囲ですが、距離を広げると回数が増えます。
検索結果は7日間キャッシュされ、同じ設定なら再検索しません。

## 制限事項

- Google Places は1地点あたり最大20件までしか返さないため、繁華街では取りこぼすことがあります
- OSMモードの精度はOpenStreetMapへの登録状況に依存します（地方のコンビニは概ね登録あり、飲食店はまちまち）
- Google Places の営業時間は表示しません（取得すると上位SKUになり無料枠が減るため）。「地図↗」で確認してください

## ライセンス

MIT License。地図タイルは OpenStreetMap（ODbL）、地図ライブラリは Leaflet（BSD-2-Clause）を利用しています。

---

## English summary

**Eat on GPX** is a single-file web app for randonneurs and touring cyclists.
Drop a GPX track and it lists convenience stores, restaurants, fast food and cafés
along the route, sorted by distance from the start, together with the GPX waypoints
(controls / checkpoints). Each spot opens in Google Maps.
Works with no API key using OpenStreetMap + Overpass; add a Google Maps API key to
switch the map and the data source to Google Maps / Places API (New).
Everything runs in the browser; the GPX file is never uploaded.
