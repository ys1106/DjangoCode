from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UserInfo(models.Model):  # 회원가입한 사용자의 정보 저장 DB 모델과
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 사용자의 정보(아이디, 비밀번호, 이메일)
    name = models.CharField(max_length=50)  # 이름
    birth = models.DateField()


class Movie(models.Model):  # 영화 정보 저장 (포스터 제외)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, null=True)  # 영화 제목
    director = models.CharField(max_length=50, null=True)  # 감독명
    year = models.CharField(max_length=5, null=True)  # 연도
    genre = models.CharField(max_length=50, null=True) #장르

    def __str__(self):
        return self.title


class Score(models.Model):  # 사용자 전체의 평점데이터 저장
    title = models.CharField(max_length=50)  # 영화 제목
    nickname = models.CharField(max_length=50)  # 사용자 아이디
    score = models.SmallIntegerField()  # 평점


class UserMovie(models.Model):  # 사용자가 추가한 영화리스트
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)  # 사용자
    movie_list = models.ManyToManyField(Movie, blank=True)  # 추가하는 영화들


class RecommendedMovie(models.Model):  # 사용자에게 추천되는 영화리스트
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)  # 사용자
    recommend_list = models.ManyToManyField(Movie, blank=True)  # 추천되는 영화들

# class PreferenceMovie(models.Model):
    # user