# スケマ！ - Keep Time to Meet -

[![Sukema Logo](./docs_img/sukema.png)](https://www.youtube.com/watch?v=e-BE-7SorJo)
 
## 製品概要 - タイムシェア x Tech -
### 背景(製品開発のきっかけ、課題等）
> 「7時に起きようと思ったらもう8時でした。」</br>
> 「2時から作用を始めようと思ったら休んだらもう4時でした。」

このように、私たち人間は時間を守ることが苦手です。何か始めようと思ってもそのことを忘れてしまいます。

しかし、誰かとの打ち合わせや相談、遊びに行くときなど、私たち人間は他人、特に上下関係のない人同士の待ち合わせには敏感に対応することができ、この瞬間だけは人が時間を守ることができるのです。

これってすごいことだと思っていて、**時間にルーズな人も待ち合わせさえあれば、積極的に時間を守ることができる**のです。

この事を利用したプロダクトとして私たちは **「スケマ！ - Keep Time to Meet -」** を開発しました。

### 製品説明（具体的な製品の説明）
スケマは「スケジュールマッチング」の略であり、言うなれば「スケジュールを軸に置いたマッチングサービス」です。同じ時間にスケジュールを登録した人同士でマッチングを行い、その時間になるとテキストチャットでお話しすることができます。

### 特長
- 5分刻みでスケジュールを登録することができます。
- その時間になるとテキストチャットに参加して会話することができます。

### 解決出来ること
- スケジュールを設定し、誰かとの待ち合わせをマッチングすることで「この時間に予定がある」という印象に残らない問題から、「この時間には待ち合わせがある」という他人の関わる問題に変えて積極的に時間を守ることができるようになります。

## デモ動画
デモ動画はYoutubeで公開しています。下のリンクから閲覧することができます。

[【JPHACKS2021成果物】スケマ！ - Keep Time to Meet -【タイムシェア × Tech】 (https://www.youtube.com/watch?v=e-BE-7SorJo)](https://www.youtube.com/watch?v=e-BE-7SorJo)

また、上のタイトル画像からもジャンプすることができます。

### 今後の展望
- 人との待ち合わせをしたそのうえで通知を飛ばせるような仕組みづくりはあるべきです。
- また、ウェブアプリだけではなくスマホアプリやウェアラブルデバイスのアプリとして制作することでより身近なアプリケーションとして成長することができるのではないかと思います。
- また、マッチングサービスである以上、運用していくうえで法律による制限も伴うのでその把握をする必要があります。

### 注力したこと（こだわり等）
開発期間がないのでどのようにして機能を限定して目的を達成するかに焦点を当てました。

## 使用技術
### Written By
<img src="./docs_img/Python_Logo.png" height=100/><img src="https://www.w3.org/html/logo/badge/html5-badge-h-css3-semantics.png" height="100" alt="HTML5 Powered with CSS3 / Styling, and Semantics" title="HTML5 Powered with CSS3 / Styling, and Semantics"/><img src="./docs_img/sass_logo.png" height=100/>

### フレームワーク・ライブラリ・モジュール
<img src="./docs_img/Flask_logo.svg.png" height=100/><img src="./docs_img/SQLite370.svg.png" height=100/><img src="./docs_img/Bootstrap_logo.svg.png" height=100/>

### 開発ツール
<img src="./docs_img/vscode.png" height=100/><img src="./docs_img/Docker_Logo.png" height=100/><img src="./docs_img/GitHub_Logo.png" height=100/><img src="./docs_img/Slack_Logo.png" height=100/><img src="./docs_img/npm-logo-red.png" height=100/>

- miro

## テスト方法
 Docker（Docker Compose）を使用する。このディレクトリで以下のコマンドを実行する。
```sh
$ docker compose build
$ docker compose up
```
その後、 `localhost:8008` をブラウザで開くとウェブアプリとして動作の確認ができる。


