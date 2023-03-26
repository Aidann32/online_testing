from django.shortcuts import render


def home(request):
    return render(request, 'landing/home.html')

def about(request):
    pass
