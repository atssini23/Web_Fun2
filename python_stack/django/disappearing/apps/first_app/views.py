from django.shortcuts import render, redirect

def index(request):
    return render(request, 'first_app/index.html')


def all(request):
    return render(request, 'first_app/all.html')


def each(request, color):
    context = {
        "color":color
    }
    return render(request, 'first_app/each.html', context)
