from django.shortcuts import render, redirect


def login(request):
    # ログイン画面
    return render(request, 'robofork_app/top/login.html', None)

    # リダイレクトする方法
    # return redirect('vehicle_index')


def index(request):
    # ログイン画面
    return render(request, 'robofork_app/top/index.html', None)

    # リダイレクトする方法
    # return redirect('vehicle_index')
