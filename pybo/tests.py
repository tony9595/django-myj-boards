from django.test import TestCase
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models import F
from django.db.models.functions import Length  # Length를 여기에서 임포트

from django.utils import timezone
from pybo.models import Answer, Question


class AggregateTestCase(TestCase):

    def setUp(self):
        """
        Test setup method to create initial data
        """
        # 질문 3개 생성
        q1 = Question.objects.create(
            subject="Python이란?",
            content="Python은 프로그래밍 언어입니다.",
            create_date=timezone.now(),
        )
        q2 = Question.objects.create(
            subject="Django란?",
            content="Django는 Python 웹 프레임워크입니다.",
            create_date=timezone.now(),
        )
        q3 = Question.objects.create(
            subject="Java란?",
            content="Java는 객체 지향 언어입니다.",
            create_date=timezone.now(),
        )

        # 각 질문에 대한 답변 생성
        Answer.objects.create(
            question=q1,
            content="Python은 매우 유용합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q1,
            content="Python은 쉽고 강력합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q2,
            content="Django는 빠르고 확장성이 좋습니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 크로스 플랫폼에서 사용됩니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 많은 라이브러리와 도구를 지원합니다.",
            create_date=timezone.now(),
        )

    # def test_value(self):
    #     ## SQL 쿼리
    #     ## SELECT subject, content  FROM Answer;
    #     ## 딕셔너리 형태로 반환
    #     result = Question.objects.values("subject", "content")
    #     result = Question.objects.all().values()  # 딕셔너리
    #     result = Question.objects.all().values_list()  # 튜플
    #     print(result)

    #     # 관련 테입즐 필드 조회(포오린키 조회)
    #     # SELECT Answer.id, Question.subject, Answer.content
    #     # FROM Answer
    #     # JOIN Question ON Answer.question_id = Question.id;
    #     query_set = Answer.objects.values("id", "question__subject", "content")
    #     print(query_set.query)

    def test_filter(self):
        # 1. 특정 ID의 질문 조회
        query = Question.objects.filter(id=1)

        # 2. 특정 제목을 가진 질문 조회
        query = Question.objects.filter(subject="Django란?")

        # 3. 특정 내용이 포함된 질문 조회 (icontains)
        query = Question.objects.filter(content__icontains="python")

        # 4. 날짜 형 조회
        # query = Question.objects.filter(create_date__gt=datetime(2024, 1, 1))

        # 5. 숫자 필터링
        # lt < x (미만), lte <= x (이하), gt > x (초과) , gte >= 5 (이상)
        query = Question.objects.filter(id__lt=5)

        # 특정 ID 사이의 질문 조회 (between)
        query = Question.objects.filter(id__range=(1, 5))

        # 2025년 1월 1일과 2025년 3월 14일 사이에 생성된 질문
        query = Question.objects.filter(create_date__range=("2025-01-01", "2025-03-14"))

        # 제목이 'Django란?' 이고, 내용에 'Django'가 포함된 질문
        query = Question.objects.filter(
            subject="Django란?", content__icontains="Django"
        )

        # 제목이 'Django란?' 이거나, 내용에 'Python이란?'인 질문 (OR 조건)
        from django.db.models import Q

        query = Question.objects.filter(
            Q(subject="Django란?") | Q(subject="Python이란?")
        )

        # 정렬
        # SELECT * FROM Question ORDER BY create_date DESC LIMIT 2;
        query = Question.objects.order_by("-id").values()[:2]

        # null 처리
        # query = Question.objects.filter(answer__isnull=False)

        # if Question.objects.filter(subject="Django란?").exists():
        #     print("해당 질문 존재")

    # annotate @ aggregate

    def test_annotate(self):

        # 각 질문별 최신 답변의 날짜 가져오기
        question = Question.objects.annotate(
            latest_answer_date=Max("answers__create_date")
        )

        # for q in question:
        #     print(q.subject, q.latest_answer_date)

        # 각 질문별, 대답의 갯수
        question = Question.objects.annotate(answer_count=Count("answers"))

        # for q in question:
        #     print(f"질문 : {q.subject}, 답변 개수: {q.answer_count}")

    def test_aggregate(self):
        # 답변 개수
        answer = Answer.objects.aggregate(total_answers=Count("id"))
        print(answer)

        # 질문 개수
        question = Question.objects.aggregate(total_questions=Count("id"))
        print(question)

        # 답변 길이 평균
        result = Answer.objects.aggregate(avg_length=Avg(Length("content")))
        print(result)

        # 가장 오래된 질문
        question = Question.objects.aggregate(old_question=Min("create_date"))
        print(question)

        # 5. 전체 답변 글자 수 합계 구하기
        result = Answer.objects.aggregate(sum_length=Sum(Length("content")))
        print(result)

        # 6. 가장 긴 질문 길이 구하기
        question = Question.objects.aggregate(long_questions=Max(Length("content")))
        print(question)

    # def test_sum_answer_ids(self):
    #     """
    #     Test for Sum aggregation on answer ids
    #     """
    #     result = Answer.objects.aggregate(Sum("id"))
    #     # SQL 쿼리:
    #     # SELECT SUM(id) FROM Answer;
    #     print(result)
    #     self.assertEqual(result["id__sum"], 15)

    def test_raw(self):
        # raw 함수 다이렉트로 sql 구문을 적을수 있도록 만든함수
        questions = Question.objects.raw("SELECT * FROM pybo_question")
        for question in questions:
            print(question.id, question.subject)

        # 특정 질문 가져오기 (id=1)
        questions = Question.objects.raw(
            "SELECT * FROM pybo_question where id = %s", [1]
        )
        for question in questions:
            print(question.id, question.subject)

        # 답변이 가장 많은 질문 가져오기
        questions = Question.objects.raw(
            """
            SELECT q.id, q.subject, COUNT(a.id) AS answer_count
            FROM pybo_question q
            LEFT JOIN pybo_answer a ON q.id = a.question_id
            GROUP BY q.id
            ORDER BY answer_count DESC
            LIMIT 1
            """
        )
        for q in questions:
            print(q.subject, q.answer_count)

        # def test_f(self):
        #     answer = Answer.objects.get(id=1)
        #     answer.content =  "aaa"
        #     answer.save()

        #     answer = Answer.objects.get(id=1)
        #     answer.content = F('content') + "aaa"
        #     answer.save()

        # #각 질문에 대해 최신 답변 날짜를 question 테이블의 필드로 업데이트
        # # UPDATE question
        # # SET latest_answer_date = (SELECT MAX(a.create_date)
        # # FROM answer a
        # # WHERE a.question_id = question.id);
        # # F()를 사용하면 Python 메모리를 사용하지 않고, DB에서 직접 연산 수행
        # #✅ JOIN과 GROUP BY 없이도 데이터를 효율적으로 업데이트 가능
        Question.objects.update(latest_answer_date=F("answer__create_date"))
