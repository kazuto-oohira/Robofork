from django.shortcuts import render, redirect


def index(request):
    return render(request, 'robofork_app/vehicle_view/index.html', None)