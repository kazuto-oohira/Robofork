from django.shortcuts import render


def login(request):
    # ログイン画面
    return render(request, 'robofork_app/login.html', None)


def index(request):
    # ログイン画面
    return render(request, 'robofork_app/top/index.html', None)
