from django.shortcuts import render
from django.template import loader


def index(request):
    return render(request, 'robofork_app/index.html', None)


def okuda(request):
    print('Okuda!!!')
    print(request.POST.get('name'))
    print(request.GET.get('name1'))

    disp_data = {
        'name1': request.POST.get('name'),
        'password1': request.POST.get('password'),
    }
    return render(request, 'robofork_app/index.html', disp_data)
