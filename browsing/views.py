from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {}
    return render(request, "browsing/index.html", context)

def register(request):
    context = {}
    return render(request, "browsing/register.html", context)

def login(request):
    context = {}
    return render(request, "browsing/login.html", context)