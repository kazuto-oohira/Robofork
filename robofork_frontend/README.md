# robofork_frontend

robofork_app で django が管理しているビューをそのまま利用しつつ、
内部で使うコンポーネント（カスタムタグ）部分のみ、こちらで開発します。

具体的には `/operation_plan/` 以下の、

* マップ画面 (src/MapViewer.vue)
* 指示画面 (src/CommandViewer.vue)

の2つを Vue.js のコンポーネントとして管理します。

このディレクトリではコンポーネントの開発環境、
並びに django 側からコンポーネントを利用できるまでのビルド方法を提供しています。



## 開発環境の動かし方

1. Node.js 8.x (あるいは 6.x 相当）の環境を整える
	* `node -v`
2. package.json の依存パッケージをインストールする
	* `npm install`
3. ローカルの開発サーバ(frontend側)を起動する
  * `cd robofork_frontend`
	* `npm run dev`
	* 8001 番ポートをすでに使用している場合は webpack.config.js の port 部分を変更する
	* この時点で以下の URL などにアクセスが可能
		* HOME 画面: <http://127.0.0.1:8001/1>
		* 運行計画明細画面: <http://127.0.0.1:8001/1/operation_plan/1>
4. Pythonの開発サーバを起動する
 	* `python manage.py runserver 0.0.0.0:8000`
	* access <http://127.0.0.1:8000>

`src/main.js` をエントリーポイントにして、
index.html から呼ばれたコンポーネントを表示しています。



## 開発環境を django に近づける

ビルド（後述）されるのは **src 以下のファイルのみです。**

例えばビルドには含めないけど jquery.js を読み込んで使いたいという場合は、
`js/jquery.js` にファイルを配置し、
`index.html` に `/js/index.js` などの script タグを追加し、
個別に読み込むことで使用可能です。

あるいは、コンポーネントの方から import して、
ビルドに含める方法もあります。

1. `npm install --save d3`
2. component.vue などのファイルから `import * as d3 from "d3";` と import して使う

こちらの場合は、ビルド後の1ファイルにまとめられます。



## django 側への反映の仕方、あるいはビルドについて

```sh
npm run build
```

以下のことが自動で行われます。

* .vue ファイル（html/css/js）のパッケージング
* minify
* django 側の適切な場所への配置 (robofork_app/static/robofork_app/js/)

### 配置場所（ファイル名）を変更したい場合

開発環境の関連ファイルとして `webpack.config.js`, `index.html` の2ファイル、
ビルドの際の関連ファイルとして `webpack.config.js` の1ファイルを編集する必要があります。



## （参考）robofork_app と robofork_frontend との統合について

それぞれの開発環境は独立しているため、
本来 frontend 側のものを毎回ビルドして robofork_app 側に持ってくる必要があります。

それでは手間であるため、django 側からフロントエンドのファイルを
リアルタイムで表示確認できるよう開発環境を統合しています。

なお、すでに環境構築済みであるため、
通常の構築手順を踏んだ場合は特別な手順は不要です。
そうでない場合は、以下の手順でアップデートしてください。

1. robofork_frontend ディレクトリ上で `npm update`
2. robofork_app ディレクトリ上で `pip install -r requirements.txt`

参考までに導入手順を記載しておきます。

1. robofork_frontend 側に、変更検知のための `webpack-bundle-tracker` を導入
  * `npm i --save-dev webpack-bundle-tracker`
2. webpack.config.js にプラグインとして読み込む記述を追加する
  * <http://owaislone.org/blog/webpack-plus-reactjs-and-django/> などを参照
  * 変更があった場合に `webpack-stats.json` というファイルで変更点を伝達する
  * `/static/robofork_app/js/` を `http://localhost:8001/static/robofork_app/js/` に変更
3. robofork_frontend のみで `webpack-stats.json` ファイルに変更があるか検証する
  * `npm run dev` で robofork_frontend 側の開発環境を立ち上げる
  * 適当にファイルを変更して、 `webpack-stats.json` に変化があることを確認する
4. robofork_app 側に、 webpack から動的に生成されたファイルを読み込む `django-webpack-loader` を導入
  * `pip install django-webpack-loader`
  * `pip freeze > requirements.txt` で変更ライブラリを requirements.txt に反映しておく
5. robofork/settings.py を編集する
  * INSTALLED_APPS に `webpack_loader` を追記する
  * WEBPACK_LOADER の記述を一番下に追加する
6. robofork_app 側のテンプレートを編集し、 robofork_frontend 側の変更を取り入れられるようにする
  * <http://owaislone.org/blog/webpack-plus-reactjs-and-django/> などを参照
  * `{% load render_bundle from webpack_loader %}` の行を上部に追加
  * `{% render_bundle 'main' 'js' %}` などで JavaScript ファイルの読み込み
7. robofork_app 側にて表示確認

### 参考 URL

* <http://owaislone.org/blog/webpack-plus-reactjs-and-django/>
* <https://github.com/ezhome/webpack-bundle-tracker>
* <https://github.com/ezhome/django-webpack-loader>
