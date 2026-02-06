from django.shortcuts import render

# Create your views here.

def hospital(request):
    return render(request, 'myapp/home.html')