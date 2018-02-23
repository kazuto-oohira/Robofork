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
3. ローカルの開発サーバを起動する
	* `npm run dev`
	* 8001 番ポートをすでに使用している場合は webpack.config.js の port 部分を変更する
	* access <http://127.0.0.1:8001>

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
