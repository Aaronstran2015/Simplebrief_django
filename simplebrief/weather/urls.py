from django.urls import path
from . import views

urlpatterns = [
    path("", views.brief, name="brief"),
    path("metar/", views.metar, name="metar"),
    path("taf/", views.taf, name="taf"),
    path("brief/", views.brief, name="brief")
]