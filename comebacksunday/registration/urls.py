from django.urls.conf import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', view=LoginView.as_view(), name='login'),
    path('logout/', view=LogoutView.as_view(), name='logout')
]