from django.shortcuts import render

def index(request):
    return render(request, 'posts/index.html')


def about(request):
    return render(request, 'about.html')