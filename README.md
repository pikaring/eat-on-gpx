# Eat on GPX

GPXファイルを読み込んで、ルート沿いのコンビニ・レストラン・ファストフード・カフェ・日帰り温泉を
地図とリスト（スタートからの距離順）で表示するWebアプリです。
各スポットは「地図↗」からGoogleマップ（iPhoneならアプリ）で開けます。

- 紹介ページ: <https://pikaring.github.io/eat-on-gpx/>
- ツール本体: <https://pikaring.github.io/eat-on-gpx/app/>

## 構成

- `index.html` … 紹介ページ（`assets/` に配色・アイコン・OGP画像）
- `app/index.html` … ツール本体（単一HTML。ビルド不要）
- `app/vendor/` … Leaflet 1.9.4（同梱。CDNが使えない・遅い環境でも地図が出るように）
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

費用の目安：Places Nearby Search は 200 km のルートで「ルートからの距離 300 m」なら約250回（100 m なら約750回、1 km なら約75回）。
Nearby Search Pro の無料枠は月5,000回程度で、超えると有料になります。Cloud Console の「割り当て」で
Places API (New) の1日あたりのリクエスト上限を設定しておけば、超過による課金を防げます。
検索結果は7日間キャッシュされ、同じ設定なら再検索しません。

## 制限事項

- Google Places は1地点あたり最大20件までしか返さないため、繁華街では取りこぼすことがあります
- OSMモードの精度はOpenStreetMapへの登録状況に依存します（地方のコンビニは概ね登録あり、飲食店はまちまち）
- Google Places の営業時間は表示しません（取得すると上位SKUになり無料枠が減るため）。「地図↗」で確認してください

## スマートフォン（特に iPhone / Safari）での動作について

モバイル回線は接続が切れやすく、Safari は保存容量の上限も小さいため、次のようにしています。

- 地図ライブラリ（Leaflet）はCDNではなく**同梱**。読み込みに失敗すると以前は画面が
  無反応のままでしたが、同一オリジンから配るようにしたうえで、失敗時はメッセージを出します
- OSMモードの検索は**ルートを約50km（最大600点）ごとに分割**して順に問い合わせます。
  1回あたりが短くなるので途中で切れにくく、`○/○ 区間` と進捗が出ます
- **一部の区間が取れなくても、取れた区間はそのまま表示**します（欠けたことを明示し、
  その結果はキャッシュしません）。全区間が失敗したときだけエラーになります
- 画面ロックやアプリ切り替えで通信が切れて失敗した場合、**画面に戻った時点で自動的に再検索**します
- 2本ずつ並行して問い合わせます（公開サーバーはIPあたり同時2本まで）。宛先は
  overpass-api.de / overpass.kumi.systems / overpass.private.coffee の3つを使い分け、
  各リクエストは**30秒**で見切りをつけ、無応答なら別サーバーに切り替えて最大4回やり直します
- **429（混雑）を返したサーバーは45秒間使わず**、待ち時間も長め（6秒→12秒→18秒）にします。
  それでも落ちた区間は、**ほかの区間が終わってからもう一度だけ取り直し**ます
  （順番待ちが解けていることが多いため）
- 検索中は「○/○ 区間・○秒」と**経過秒**を表示し、「再検索」ボタンが**「✕ 中止」**に変わります。
  待たされたときは中止でき、そこまでに取得できた区間は表示されます
- iOSの「設定 → Safari → IPアドレスを非公開」（iCloudプライベートリレー）がオンだと共有IPになり、
  IP単位でスロットを配る Overpass では順番待ちに入りやすくなります。タイムアウトが続くときは
  この設定を切って試してください（アプリ側でもその旨を表示します）
- 設定・検索キャッシュの保存に失敗しても動作は止まりません（プライベートブラウズでも利用可。
  容量不足のときは古い検索キャッシュを自動で捨てます）
- iOS の「ファイル」アプリで .gpx が選べないこと（灰色表示）があるため、iPhone / iPad では
  ファイル選択の種類しぼり込み（accept）を外しています
- iCloud Drive にあって端末にダウンロードされていないファイルは読み込めません。
  その場合は先に端末へダウンロードしてから選んでください

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
