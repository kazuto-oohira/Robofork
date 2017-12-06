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
    which = models.my_view(request)
    
    # ユーザーと一致した場合 本来のページに移動
    if which == 1:
        return render(request, 'robofork_app/redirect.html', disp_data)

    # ユーザーと一致しない場合 index.htmlに移動
    else:
        return render(request, 'robofork_app/index.html', disp_data)
