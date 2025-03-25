from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from pybo.models import Answer, Question
from pybo.forms import AnswerForm, QuestionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def index(request):

    print(request.user)

    page = request.GET.get("page", "1")  # 페이지

    question_list = Question.objects.order_by("-create_date")

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {"question_list": page_obj}
    # context = {"question_list": question_list}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        return HttpResponseNotAllowed("Only post is possible")

    context = {"question": question, "form": form}

    return render(request, "pybo/question_detail.html", context)


def question_create(request):

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


def set_cookie_view(request):
    response = HttpResponse("쿠키가 설정되었습니다.")
    response.set_cookie("my_cookie", "cookie_value", max_age=3600)  # 1시간 유지
    return response


def get_cookie_view(request):
    cookie_value = request.COOKIES.get("my_cookie", "쿠키가없습니다.")
    return HttpResponse(f"쿠키값:{cookie_value}")


def delete_cookie_view(request):
    response = HttpResponse("쿠키가 삭제되었습니다.")
    response.delete_cookie("my_cookie")
    return response


def set_session_view(request):
    request.session["username"] = "DjangoUser"
    request.session.set_expiry(3600)
    return HttpResponse("세션이 설정되었습니다.")


def get_session_view(request):

    from django.contrib.sessions.models import Session
    from django.contrib.sessions.backends.db import SessionStore

    # 특정 세션 키 조회
    session_key = "s36qojk9lnuwnnc5ryy5a5ok2k86zemo"  # 실제 저장된 session_key 입력
    session = Session.objects.get(session_key=session_key)

    # 세션 데이터 복호화
    session_data = SessionStore(session_key=session_key).load()
    print(session_data)  # {'username': 'DjangoUser'}

    username = request.session.get("username", "세션이 없습니다.")
    return HttpResponse(f"세션값: {username}")


def delete_session_view(request):
    request.session.flush()
    return HttpResponse("세션이 삭제 되었습니다.")


@login_required(login_url="common:login")
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정권한이없습니다")
        return redirect("pybo:detail", question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question.id)

    else:
        form = QuestionForm(instance=question)

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("pybo:detail", question_id=question_id)
    question.delete()
    return redirect("pybo:index")
