from django.db import models
from django.contrib.auth import authenticate, login
from . import views
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Authority:
    class Meta:
        permissions = (
            ("plan", "Can plan available Tasks"),
            ("manage", "Can manage and check the status of Vehicle and Task"),
            ("usr", "Can do Task for Vehicle"),
        )

##### Loginできるか判定 #####
def usercheck(request):
    from django.contrib.auth import authenticate
    from django.contrib.auth.decorators import permission_required
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
    print(user)

    # user != None -> success login
    if user is not None:
        print('success login, welcome')
        login(request, user)
        AuthorityPlan = user.has_perm('Meta.plan')
        AuthorityManage = user.has_perm('Meta.manage')
        AuthorityUsr = user.has_perm('Meta.usr')
        if AuthorityPlan == 1:
            which = 3
        if AuthorityManage == 1:
            which = 2
        else:
            which = 1

        # Test用
        print(AuthorityPlan)
        print(AuthorityManage)
        print(AuthorityUsr)

    # user = None -> failed login
    else:
        print('unsuccess login, please correct data')
        which = 0

    return which