from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils import timezone
from pybo.models import Answer, Question
from pybo.forms import QuestionForm


# Create your views here.


def index(request):
    question_list = Question.objects.order_by("-create_date")
    context = {"question_list": question_list}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    content = request.POST.get("content")
    question.answer_set.create(content=content, create_date=timezone.now())

    # answer = Answer(question=question, content=content, creatdate_date=timezone.now())
    # answer.save()

    return redirect("pybo:detail", question_id=question_id)


def question_create(request):

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()
        return render(request, "pybo/question_form.html", {"form": form})
