from django.contrib import admin
from django.urls import path, include

from pybo import views

app_name = "pybo"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("answer/create/<int:question_id>/", views.answer_create, name="answer_create"),
    path("question/create/", views.question_create, name="question_create"),
    path("get-cookie/", views.get_cookie_view, name="get_cookie"),
    path("set-cookie/", views.set_cookie_view, name="set_cookie"),
    path("delete-cookie/", views.delete_cookie_view, name="delete_cookie"),
    path("set-session/", views.set_session_view, name="set_session"),
    path("get-session/", views.get_session_view, name="get_session"),
    path("delete-session/", views.delete_session_view, name="delete_session"),
]
