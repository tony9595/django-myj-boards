from django.shortcuts import render
from django.http import HttpResponse

from pybo.models import Question

# Create your views here.


def index(requst):
    question_list = Question.objects.order_by("-create_date")
    context = {"question_list": question_list}
    return render(requst, "pybo/question_list.html", context)
