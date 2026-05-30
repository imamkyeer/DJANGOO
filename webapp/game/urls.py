from django.urls import path
from . import views

urlpatterns = [
    # index / page awalnya
    path('', views.index),
    # halaman / moba
    path('moba', views.moba),
    # halaman / genshin
    path('genshin', views.genshin),
    # halaman / dota
    path('dota', views.dota),
]