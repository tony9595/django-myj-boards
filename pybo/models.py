from django.db import models

# Create your models here.


# dev_2
class Question(models.Model):
    subject = models.CharField(max_length=100)
    # 글자 수에 제한이 없는 텍스트는 TextField를 사용한다
    content = models.TextField()
    create_date = models.DateTimeField()


class Answer(models.Model):
    # 1 : N Qustion객체를 가져온다.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
