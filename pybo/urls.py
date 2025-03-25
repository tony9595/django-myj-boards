from django.contrib import admin
from django.urls import path, include

from pybo.views import *

app_name = "pybo"

urlpatterns = [
    path("", index, name="index"),
    path("<int:question_id>/", detail, name="detail"),
    path("answer/create/<int:question_id>/", answer_create, name="answer_create"),
    path("question/create/", question_create, name="question_create"),
    path(
        "question/modify/<int:question_id>/",
        question_modify,
        name="question_modify",
    ),
    path(
        "question/delete/<int:question_id>/",
        question_delete,
        name="question_delete",
    ),
    path(
        "answer/modify/<int:answer_id>/",
        answer_modify,
        name="answer_modify",
    ),
    path(
        "answer/delete/<int:answer_id>/",
        answer_delete,
        name="answer_delete",
    ),
]
