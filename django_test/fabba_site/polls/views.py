from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi. I'm Fab. You are viewing the polls index")


def detail(request, question_id):
    response = f"You are looking at question {question_id}"
    return HttpResponse(response)


def results(request, question_id):
    response = f"You are looking at the results of question {question_id}"
    return HttpResponse(response)


def vote(request, question_id):
    response = f"You are voting on question {question_id}"
    return HttpResponse(response)
