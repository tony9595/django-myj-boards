from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from pybo.models import Answer, Question
from pybo.forms import AnswerForm, QuestionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


def index(request):
    # print(request.user)

    page = request.GET.get("page", "1")  # 페이지

    kw = request.GET.get("kw", "")

    question_list = Question.objects.order_by("-create_date")

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw)  # 질문 제목 검색
            | Q(content__icontains=kw)  # 질문 내용 검색
            | Q(answer__content__icontains=kw)  # 답변 내용 검색
            | Q(author__username__icontains=kw)  # 질문 작성자 검색
            | Q(answer__author__username__icontains=kw)  # 답변 작성자 검색
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {"question_list": page_obj, "page": page, "kw": kw}
    # context = {"question_list": question_list}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)
