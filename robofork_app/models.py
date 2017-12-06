from django.db import models
from django.contrib.auth import authenticate, login
from . import views

##### Test↓ #####
def usercheck(request):
    from django.contrib.auth import authenticate
    user = authenticate(username='john', password='secret')
    if user is not None:
        # A backend authenticated the credentials
        print('true')
    else:
        # No backend authenticated the credentials
        print('false')

##### ↑Test #####

def my_view(request):
    username = request.POST.get('name')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        print('true')
        return 1
    else:
        print('false')
        return 0