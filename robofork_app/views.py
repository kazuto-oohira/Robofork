from django.shortcuts import render
from django.template import loader
from django.contrib.auth import authenticate, login
from . import models

def index(request):
    return render(request, 'robofork_app/index.html', None)

def redirect(request):
    disp_data = {
        'name': request.POST.get('name'),
        'password': request.POST.get('password'),
    }
    # models.pyにてログイン判定
    # 権限がuserの場合
    which = models.my_view(request)
    print(which)
    if which == 1:
        return render(request, 'robofork_app/usr.html', None)
    # 権限がmanageの場合
    if which == 2:
        return render(request, 'robofork_app/manage.html', None)
    # 権限がNKC(planer)の場合
    if which == 3:
        return render(request, 'robofork_app/plan.html', None)
    # ユーザーと一致しない場合 index.htmlに移動（正しい値を入力するように促しても良い）
    else:
        return render(request, 'robofork_app/index.html', None)

# logout用 test
def logout(request):
    disp_data = {
        'name': request.POST.get('name'),
        'password': request.POST.get('password'),
    }
    return render(request, 'robofork_app/logout.html', disp_data)