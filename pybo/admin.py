from django.contrib import admin

from pybo.models import Question

# 관리자 화면에서 제목(subject)으로 질문 데이터를 검색

# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["subject"]


admin.site.register(Question, QuestionAdmin)
