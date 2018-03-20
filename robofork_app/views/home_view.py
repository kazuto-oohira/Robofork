from django.shortcuts import render, redirect

def index(request, location_id):
    # 車両取得


    return render(request, 'robofork_app/home/index.html', {'vehicles': None})
