from django.shortcuts import render


def index(request):
    """
    トップ画面。全ての起点
    :param request:
    :return:
    """
    return render(request, 'robofork_app/top/index.html', None)
