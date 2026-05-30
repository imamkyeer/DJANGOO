from django.urls import path
from . import views

urlpatterns = [
path("index~", views.santri_home),
    path("biodata", views.biodata),
    path("jadwal", views.jadwal, ),
    path("galeri", views.galeri,),
    path("feedback", views.feedback,),
]