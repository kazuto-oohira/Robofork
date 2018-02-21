# Robofork

## 開発環境の動かし方

1. Python 3.4, Django 2.0 以上の環境を整える
	* see <https://docs.djangoproject.com/ja/2.0/faq/install/#faq-python-version-support>
	* `python -V`
	* `python -m django --version`
2. requirements.txt の依存パッケージをインストールする
	* `pip install -r requirements.txt`
3. 初回の場合、 migration （DB 作ったり最新に合わせたり）を実行する
	* `python manage.py migrate`
4. ローカルの開発サーバを起動する
	* `python manage.py runserver`
	* 8000 番ポートをすでに使用している場合は末尾に別のポート番号をつける
	* access <http://127.0.0.1:8000>
