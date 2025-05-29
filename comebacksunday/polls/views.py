from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Question

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', context={
        "question": question
    })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    return render(request, 'polls/results.html', context={
        "choices": choices
    })