from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView

# Create your views here.
def logout_view(request) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'posts/logout.html')
    elif request.method == "POST":
        return LogoutView.as_view()(request)
    else:
        response = HttpResponse("Unsupported method.", headers = {"Allowed": "GET, POST"})
        response.status_code = 405
        return response