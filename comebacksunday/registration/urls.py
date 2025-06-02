from django.urls.conf import path
from django.contrib.auth.views import LoginView
from .views import logout_view

urlpatterns = [
    path('login/', view=LoginView.as_view(), name='login'),
    path('logout/', view=logout_view, name='logout')
]