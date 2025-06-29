from django.shortcuts import render

# Create your views here.

def motus(request):
    return render(request, 'motus/home.html')