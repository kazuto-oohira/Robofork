from django.shortcuts import render, redirect


def index(request):
    """
    トップ画面。全ての起点
    :param request:
    :return:
    """

    # 直接ログイン画面を開く方法
    # return render(request, 'robofork_app/top/index.html', None)
    # リダイレクトする方法
    return redirect('vehicle_index')
