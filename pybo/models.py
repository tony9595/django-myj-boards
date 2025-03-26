from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# dev_2
class Question(models.Model):

    # author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_question"
    )
    # 필드가 null로 저장되는 것을 허용 null=True | blank=True
    subject = models.CharField(max_length=100)
    # 글자 수에 제한이 없는 텍스트는 TextField를 사용한다
    content = models.TextField()
    create_date = models.DateTimeField()
    # modify 칼럼에 null 허용
    # blank=True 는 formis_valid()를 통한 입력 데이터 검증 시 값이 없어도 된다는 의미
    modify_date = models.DateField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name="voter_question")

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 1 : N Qustion객체를 가져온다.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateField(null=True, blank=True)
