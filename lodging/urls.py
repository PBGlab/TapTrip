from django.urls import path
from lodging import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^booking/',views.booking,name="booking"),
    url(r'^lodging/',views.lodging,name="lodging"),
    # path("stream_hotels/", views.stream_hotels, name="stream_hotels"),
]