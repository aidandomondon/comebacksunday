from django.urls.conf import path
from django.contrib.auth.views import LoginView
from .views import logout_view

app_name = 'registration'

urlpatterns = [
    path('login/', view=LoginView.as_view(), name='login'),
    path('logout/', view=logout_view, name='logout')
]
print(LoginView.next_page)