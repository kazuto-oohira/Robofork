# Robofork

## 開発環境の動かし方

1. Python 3.6 以上の環境を整える
	* see <https://docs.djangoproject.com/ja/2.0/faq/install/#faq-python-version-support>
	* `python -V`
2. requirements.txt の依存パッケージをインストールする
	* `pip install -r requirements.txt`
	* `python -m django --version`
3. 初回の場合、 migration （DB 作ったり最新に合わせたり）と初回データ投入を実行する
	* `python manage.py migrate`
	* `python manage.py loaddata initial_data_20180318.yaml`（他にもあるかも。`robofork_app/fixures`ディレクトリの全ファイルをやる）
4. ローカルの開発サーバを起動する
	* `python manage.py runserver 0.0.0.0:8000`
	* 8000 番ポートをすでに使用している場合は末尾に別のポート番号をつける
	* access <http://127.0.0.1:8000>
	* 開発用の別設定を使う場合（MQTTサーバーをローカルに立てる場合等）
	    * `robofork/settings.py`が設定ファイル。`robofork/settings-dev.py`という名前でコピーして、MQTTサーバーのIPアドレスなどを変更する。（`robofork/settings-dev.py`は`.gitignore`に定義されているので独自に作ってもGitに影響はない）
	    * 開発用の設定ファイルを使う場合、`python manage.py runserver 0.0.0.0:8000 --settings=robofork.settings-dev`として起動する。
5. (Option)ローカルのMQTTサーバーを起動する
    * インストールは、`brew install mosquitto`で行う。`Homebrew`は別途調べてね。
    * MQTTサーバーの起動は`/usr/local/sbin/mosquitto`で起動する。特に設定は不要だった。

一部マップ表示を用いるページなどについては、
別途フロントエンドのフレームワークを導入しており、
詳しくは [robofork_frontend/README.md](robofork_frontend/README.md) を参照のこと。
