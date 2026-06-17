from django.shortcuts import render, redirect, get_object_or_404
from .models import perpus_db
from django.http import HttpResponse

def index(request):
    return render("Halo Perpustakaan")