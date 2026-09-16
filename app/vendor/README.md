# vendor

同梱している外部ライブラリ。CDNが遅い・詰まる・ブロックされる環境でも地図が出るように、
同一オリジンから配っています（ローカルでHTMLを開いたときもそのまま動きます）。

| ファイル | 内容 | 取得元 | ライセンス |
|---|---|---|---|
| `leaflet-1.9.4.min.js` / `.css` | Leaflet 1.9.4 | https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/ | BSD-2-Clause |
| `images/*.png` | Leaflet 付属画像 | 同上 | BSD-2-Clause |

更新するときは同じURLのバージョン部分を差し替えて取得し、`app/index.html` の
`<link>` / `<script>` のファイル名も合わせてください。
