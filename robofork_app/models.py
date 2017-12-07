from django.db import models
from django.contrib.auth import authenticate, login
from . import views

##### Loginできるか判定 #####
def usercheck(request):
    from django.contrib.auth import authenticate
    user = authenticate(username='john', password='secret')
    if user is not None:
        # A backend authenticated the credentials
        print('true')
    else:
        # No backend authenticated the credentials
        print('false')

# login&権限認証
# 構文がよくわからない、今は数字を返している
def my_view(request):
    username = request.POST.get('name')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    # user != None -> success login
    if user is not None:
        print('success login, welcome')
        login(request, user)
        # 権限判定で飛ばすページを選ぶ
        #
        #
        #
        #
        #
        #

        which = 1

        return which

    # user = None -> failed login
    else:
        print('unsuccess login, please correct data')
        return 0