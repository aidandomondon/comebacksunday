from django.urls.conf import path
from django.contrib.auth.views import LoginView
from .views import logout_form_view

urlpatterns = [
    path('login/', view=LoginView.as_view(), name='login'),
    path('logout_form/', view=logout_form_view, name='logout_form')
]