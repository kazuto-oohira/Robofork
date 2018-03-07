from django.shortcuts import render, redirect


def index(request):
    """
    トップ画面。全ての起点
    :param request:
    :return:
    """

    # ログイン画面
    return render(request, 'robofork_app/top/index.html', None)

    # リダイレクトする方法
    # return redirect('vehicle_index')
