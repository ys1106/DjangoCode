import json
import random
import numpy as np
import pandas as pd
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from sklearn.metrics.pairwise import cosine_similarity

from users.forms import LoginForm, SignupForm
from users.models import UserInfo, Movie, Score, UserMovie, RecommendedMovie


# Create your views here.


# 로그인 페이지
def login_page(request):  # post 방식이면
    if request.user.is_authenticated:  # 로그인 되어 있다면
        return redirect('http://13.125.139.101/mypage')  # mypage

    if request.method == 'POST':
        form = LoginForm(request.POST)  # 로그인 폼
        if form.is_valid():  # 유효성 검사
            user_id = form.cleaned_data.get('userid')  # 입력받은 아이디
            user_password = form.cleaned_data.get('password')  # 입력받은 비밀번호

            try:  # 입력한 아이디를 가진 사용자가 있는지 확인
                User.objects.get(username=user_id)
            except:
                err = '아이디 또는 비밀번호를 다시 확인하세요.'
                return render(request, 'registration/login.html', locals())

            login_user = authenticate(username=user_id, password=user_password)  # 로그인 하려는 사용자 가져옴

            if login_user is not None:  # 로그인 하려는 사용자가 존재하지 않는다면
                login(request, login_user)  # 로그인 실행
                return redirect('http://13.125.139.101/mypage')
            else:  # 없으면 에러메시지
                err = '아이디 또는 비밀번호를 다시 확인하세요.'
        return render(request, 'registration/login.html', locals())
    form = LoginForm()

    return render(request, 'registration/login.html', locals())


# 회원가입 페이지
def signup_page(request):
    if request.user.is_authenticated:  # 이미 로그인이 되어 있으면
        redirect('http://13.125.139.101/mypage')  # mypage로

    if request.method == 'POST':
        form = SignupForm(request.POST)  # 회원가입폼 가져옴
        if form.is_valid():  # 유효성 검사
            try:
                user_password = form.password_check()  # 입력한 password 두 개가 일치하는지 확인하는 함수 -> 일치하면 그 비밀번호 저장
            except:  # 입력한 두 비밀번호가 다르면
                err = '두 비밀번호가 다릅니다.'
                return render(request, 'registration/signup.html', locals())  # 회원가입 페이지로 다시 이동

            user_id = form.cleaned_data.get('userid')
            try:
                User.objects.get(username=user_id)
                err = '있는 아이디입니다 ^0^'
                return render(request, 'registration/signup.html', locals())
            except:
                pass

            user_name = form.cleaned_data.get('name')
            user_email = form.cleaned_data.get('email')
            user_birth = form.cleaned_data.get('birth')

            try:
                signup_user = User.objects.create_user(username=user_id, email=user_email, password=user_password)
                # signup_user.save() # ??
                # info_user = User.objects.create(user=signup_user, name=user_name, birth=user_birth) # ??
                # info_user.save() # ??
                return redirect(reverse('index'))
            except:
                err = '에러?'
                return render(request, 'registration/signup.html', locals())

            # signup_user.save()
            # info_user = UserInfo.objects.create(user=signup_user, name=user_name, birth=user_birth)
            # info_user.save()

        err = '회원가입이 실패하였습니다.'
        return render(request, 'registration/signup.html', locals())

    form = SignupForm()
    return render(request, 'registration/signup.html', locals())


# 로그아웃
def logout_page(request):
    logout(request)  # 로그아웃 함수
    return redirect(reverse('index'))


# ??
def index(request):
    return render(request, 'index.html', locals())


def my_page(request):
    try:
        user_movie_list = UserMovie.objects.get(user=request.user).movie_list.all()  # 현재 로그인 되어있는 사용자의 영화리스트
    except:  # 없으면
        pass

    try:
        recom_movie_list = RecommendedMovie.objects.get(
            user=request.user).recommend_list.all()  # 현재 로그인 되어있는 사용자의 추천리스트
    except:  # 없으면
        pass

    # user_list = {'user_movies': user_movie_list}
    # recom_list = {'recom_movies': recom_movie_list}
    # return render(request, 'registration/mypage.html', user_list, recom_list)
    return render(request, 'registration/mypage.html', locals())


# def mypage_add(request):
#
#     total_movie_list = Movie.objects.all()[:20]
#     for movie in total_movie_list:
#         movie.img = join(MEDIA_URL, movie.id+'.jpg')
#     # movie_list = {'total_movie_list': total_movie_list}
#
#     return render(request, 'registration/addpage.html', locals())

## -- 현재 로그인되어 있는 사용자 정보도 가져와야함
# try:
#     user_movies = UserMovie.objects.get(user=request.user)  # 현재 로그인되어 있는 사용자의 영화리스트 불러옴
# except:  # ?
#     pass
# try:
#     recom_list =
# except:


# if request.method == 'POST':
#
# def movie(request, id):
#     movie = Movie.objects.get(id=id)
#     dictionary = {
#         'id': movie.id,
#         'director': movie.director,
#         'genre': movie.genre,
#         'title': movie.title,
#     }
#     return HttpResponse(str(dictionary), content_type=u"application/json; charset=utf-8")


# def movies(request):
#     ids = request.POST['id']
#     # {'id': [1,2,3,4,5,6,7]} # 보낼 때
#     return json.dumps(get_movies(ids))


def get_movies(ids):
    ids = [str(x) for x in ids]
    movies = Movie.objects.filter(id__in=ids)
    li = []
    for movie in movies:
        dictionary = {
            'id': movie.id,
            'title': movie.title,
            'director': movie.director,
            'genre': movie.genre,
        }
        li.append(dictionary)
    return li


# @csrf_exempt
def random_movies(request):
    # test_ids = random.choice(test)
    # ids = [random.randint(0, Movie.objects.count()) for x in range(20)]

    # except_list = request.POST['']
    id_list = list(Movie.objects.values_list('id'))
    # id_list.removie(except_list)
    ids = [random.choice(id_list)[0] for x in range(20)]
    return HttpResponse(get_movies(ids), content_type=u"application/json; charset=utf-8")


def test_add_mymovie(request):
    movie_list = {'movies': [{'id': 999,
                             'score': 10},
                            {'id': 33,
                             'score': 10}
                            ]
                    }
    print(movie_list['movies'][0]['id'])
    #
    # print(movie_list['id'])
    # try:
    #     login_movies = UserMovie.objects.get(user=request.user)
    # except:
    #     login_movies = UserMovie.objects.create(user=request.user)
    #
    # print(login_movies.movie_list)
    # for movie in movie_list:
    #     movie_id = movie['id']
    #     movie_score = movie['score']
    #     print(movie_id, movie_score)
    #     print(request.user.username)
    #     try:
    #         movie_ob = Movie.objects.get(id=movie_id)
    #     except:
    #         movie_ob = Movie.objects.create(id=movie_id)  # 실행되면 안됨??
    #
    #     scores = Score.objects.create(nickname=request.user.username, title=movie_ob.title, score=movie_score)
    #     print(scores.title, scores.nickname, scores.score)
    #     # scores.save()
    #     try:
    #         login_movies.movie_list.get(movie_ob)
    #     except:
    #         login_movies.movie_list.add(movie_ob)
    #     print(login_movies.user, login_movies.movie_list)
    return HttpResponse(movie_list, content_type=u"application/json; charset=utf-8")


def get_my_movies(request):  # 로그인유저의 마이리스트
    li = []
    try:
        user_movies = UserMovie.objects.get(user=request.user)
        print(user_movies.movie_list)
        for movie in user_movies.movie_list.all():
            dictionary = {
                'id': movie.id,
                'title': movie.title,
                'director': movie.director,
                'genre': movie.genre,
                # 'img': {% static 'media/' %}{{ movie.id }}.jpg,
            }
            li.append(dictionary)
    except:  # 마이리스트가 없으면 (추가 전)
        pass
    return HttpResponse(li, content_type=u"application/json; charset=utf-8")


def get_recom_movies(request):  # 로그인유저의 추천리스트
    li = []
    try:
        recom_movies = RecommendedMovie.objects.get(user=request.user)
        print(recom_movies.recommend_list)
        for movie in recom_movies.recommend_list.all():
            dictionary = {
                'id': movie.id,
                'title': movie.title,
                'director': movie.director,
                'genre': movie.genre,
            }
            li.append(dictionary)
    except:  # 추천 리스트가 없으면(추가하기 전)
        pass

    return HttpResponse(li, content_type=u"application/json; charset=utf-8")


@csrf_exempt
def add_my_movies(request):  # 추가하기 페이지에서 넘어오는 데이터 받아서 실행
    if request.method == 'POST':
        # print(request.POST)
        movie_list = request.POST.get('addmovies', '')
        try:
            login_movies = UserMovie.objects.get(user=request.user)
        except:
            login_movies = UserMovie.objects.create(user=request.user)
        # scores = Score.objects.create(nickname=request.user.username)

        for movie in movie_list:
            movie_id = movie['id']
            movie_score = movie['score'] * 10  # 1~5 -> 10~100

            try:
                movie_ob = Movie.objects.get(id=movie_id)
                scores = Score.objects.create(nickname=request.user.username, title=movie_ob.title, score=movie_score)
                # print(scores.title, scores.nickname, scores.score)
                login_movies.movie_list.add(movie_ob)
                print(login_movies.user, login_movies.movie_list)
            except:
                pass

        # 추천받기 알고리즘 실행
        recommend_movies(request)
        return HttpResponse('success')
    return HttpResponse('success')

# def vue_mypage():


# 추천받기
# def get_login_user(request):  # 여기서는 필요X??
#     return HttpResponse(str(request.user.username))

# def get_score_data():  # 평점 데이터 DB에서 가져오기
#     total_scores = list(Score.objects.all().values())
#     total_scores = pd.DataFrame(total_scores)  # ???
#     total_scores.sort_values('title', inplace=True)
#     total_scores.reset_index(drop=True, inplace=True)
#     print('total_scores', total_scores) # total_scores에서 id 삭제해야??
#     return total_scores
#
#
# def get_groupby_data():  # get_score_data()에서 가져온 데이터 형태 변경
#     total_scores = get_score_data()
#     groupby_scores = total_scores.groupby(['nickname', 'title'])['score'].max().unstack()
#     groupby_scores.fillna(0, inplace=True)
#     groupby_scores = groupby_scores.astype('float32')
#     print('groupby_scores',groupby_scores)
#     return groupby_scores
#
#
# def cosine_matrix():  # 코사인 유사도 행렬 리턴
#     score_matrix = get_groupby_data()
#     # 코사인 유사도
#     groupby_score_T = score_matrix.transpose()
#     cos_array = cosine_similarity(groupby_score_T, groupby_score_T)
#     cos_matrix = pd.DataFrame(data=cos_array, index=score_matrix.columns, columns=score_matrix.columns)
#     print('cos_matrix',cos_matrix)
#     return cos_matrix


def fpredict_scores_one(request):  # 사용자 한 명에 대한 예측평점 행렬 구하기
    # login_id = get_login_user()
    # cos_arr = cosine_matrix().values
    # groupby_scores = get_groupby_data()
    login_id = request.user.username
    cos_matrix = pd.read_csv(r'C:\Users\yousu\PycharmProjects\SW2019test1_\cos_matrix.csv', encoding='utf-8')  # ??????
    cos_matrix.set_index('title', inplace=True)
    print('cos_matrix', cos_matrix)
    # groupby_scores = pd.read_csv(r'C:\Users\yousu\PycharmProjects\SW2019test1_\groupby_scores.csv', encoding='utf-8')  #?????
    ########################
    # groupby scores 파일 안부르고 로그인 유저의 영화평점만 가져오기
    # groupby scores 영화목록(cosine_sim.py에서 movie_title.csv로 내보내기_index가title/값이0인 df)
    scores_login = pd.read_csv(r'C:\Users\yousu\PycharmProjects\SW2019test1_\scores_for_user.csv', encoding='utf-8')
    scores_login.set_index('title', inplace=True)
    print('scores_login', scores_login)
    # 로그인 유저의 평점데이터
    scores = list(Score.objects.filter(nickname=request.user.username))  # try?
    for score in scores:
        scores_login.loc[score.title]['score'] = float(score.score)

    cos_arr = cos_matrix.values
    # score_series = groupby_scores.loc[login_id]
    # score_arr = score_series.values
    score_arr = scores_login.values.ravel()
    num = 20

    # predict_matrix = pd.DataFrame(np.zeros(score_arr.shape), index=score_series.index)
    predict_matrix = pd.DataFrame(np.zeros(score_arr.shape), index=scores_login.index)
    predict_matrix = predict_matrix.astype('float32')

    for ind in range(score_arr.shape[0]):
        # top_n = np.array(np.array(cos_matrix.iloc[:, col]).argsort()[-2:-num - 2:-1])
        # ## 자기자신을 제외하기 위해 인덱싱 변경??? (자기자신과의 유사도가 1이니까)
        top_n = np.argsort(cos_arr[:, ind])[:-num - 1:-1]
        print(ind)
        predict_matrix.iloc[ind] = cos_arr[ind, :][top_n].dot(np.transpose(score_arr[top_n]))
        predict_matrix.iloc[ind] /= np.sum(np.abs(cos_arr[ind, :][top_n]))

    predict_matrix.to_csv('predict_matrix' + login_id + '.csv', encoding='utf-8-sig')

    print('predict_matrix', predict_matrix)

    # 유저가 안 본 리스트
    # user_rating = groupby_scores.loc[login_id, :]
    already_seen = scores_login[scores_login['score'] > 0].index.tolist()
    movie_list = scores_login.index.tolist()  # 모든 영화명
    unseen_list = [movie for movie in movie_list if movie not in already_seen]
    print('unseen_list', unseen_list)
    return predict_matrix, unseen_list


# def get_unseen_movies(request):  # 사용자가 보지 않은 영화 리스트 가져오기
#     scores_matrix = get_groupby_data()
#     # userid = get_login_user()
#     userid = request.user.username
#
#     user_rating = scores_matrix.loc[userid, :]
#
#     already_seen = user_rating[user_rating > 0].index.tolist()
#
#     movie_list = scores_matrix.columns.tolist() # 모든 영화명
#
#     unseen_list = [movie for movie in movie_list if movie not in already_seen]
#
#     print('unseen_list',unseen_list)
#     return unseen_list


def recommend_movies(request):  # 영화 추천_예측평점 행렬에서 topn개 가져오기
    predict_matrix_one_user, unseen_list_one_user = predict_scores_one(request)  # 로그인된 유저의 예측평점 행렬 & 안 본 영화리스트
    # unseen_list_one_user = get_unseen_movies(request)
    topn = 5
    recom_movies = predict_matrix_one_user.loc[unseen_list_one_user].sort_values([0], ascending=False)[:topn]
    print(recom_movies)
    # 추천된 영화리스트 RecommendedMovie DB에 넣기
    try:  # 현재 로그인 되어있는 사용자 RecommendedMovie 객체 가져옴
        user_recom = RecommendedMovie.objects.get(user=request.user)
    except:  # 없으면 생성 (처음 추천받는 경우)
        user_recom = RecommendedMovie.objects.create(user=request.user)
    for movie_title in list(recom_movies.index):  # 추천영화리스트에 있는 영화제목
        try:
            recom_movie = Movie.objects.get(title=movie_title)  # 영화 객체 가져옴
            user_recom.recommend_list.add(recom_movie)
        except:
            pass
        print(recom_movies)
    return HttpResponse(recom_movies, content_type=u"application/json; charset=utf-8")
