from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.index),
    path('blog/detail', views.detail)
]
