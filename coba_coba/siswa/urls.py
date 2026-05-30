from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tambah/', views.tambah, name='tambah'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('hapus/<int:id>/', views.hapus, name='hapus'),
]