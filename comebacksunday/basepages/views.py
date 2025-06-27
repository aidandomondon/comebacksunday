from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def welcome_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'basepages/welcome_page.html')