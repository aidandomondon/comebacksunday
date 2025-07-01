
from django.urls import path
from . import views

app_name="basepages"

urlpatterns = [
    path('', views.welcome_page, name="welcome_page")
]