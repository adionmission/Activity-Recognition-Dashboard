from django.urls import path
from . import views

# used when someone calls for home page
urlpatterns = [
    path("", views.index, name="index")
]
