from django.urls import path
from attractions import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^findattractions/',views.findattractions,name="findattractions"),
    url(r'^showattractions/',views.showattractions,name="showattractions"),
]