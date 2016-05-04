from django.shortcuts import render

def home(request):
    return render(request, "home.html", {})

def home2(request):
    return render(request, "home2.html", {})

def home3(request):
    return render(request, "home3.html", {})
