# /pyapp/static

- 静的ページを置くディレクトリです。

## 環境構築方法
- nodejsを使用します。
```sh
npm install
npm run hot-reload
```

## 絶対パスで埋め込む方法
以下のような形で行う
```sh
{{ abs_path("partials/headend.html") | safe }}
```