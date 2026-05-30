from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# index = / = halaman utama
def index(request):
    return HttpResponse("<h1>Hello World via Django!</h1>")

def detail(request):
    return HttpResponse("<h1>Halaman Detail Bang!</h1>")
