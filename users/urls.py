from django.urls import path, include

from users import views as users_views
# from users.recommendation import get_login_user

app_name = 'users'

urlpatterns = [
    # html (page)
    path('login/', users_views.login_page, name='login'),
    path('logout/', users_views.logout_page, name='logout'),
    path('signup/', users_views.signup_page, name='signup'),
    path('mypage/', users_views.my_page, name='mypage'),
    # path('mypageadd/', users_views.mypage_add, name='mypageadd'),


    # path('vuemypage/', users_views.vue_mypage, name='vuemypage'),

    path('recommend_movies/', users_views.recommend_movies, name='recommendmovies'),  # ? 마이페이지에서 추천받기 클릭하면 실행
    path('addmymovies/', users_views.add_my_movies, name='addmymovies'),  # ? 추가하기 페이지에서 영화들 선택 후 실행

    # api (data)33333
    # path('movie/<int:id>', users_views.movie, name='movie'),
    # path('movies/', users_views.movies, name='movies'), 
    path('randommovies/', users_views.random_movies, name='randommovies'),  # 영화정보
    path('mymovies/', users_views.get_my_movies, name='getmymovies'),  # ? 로그인 유저의 mylist
    path('recommovies/', users_views.get_recom_movies, name='recommovies'),  # ? 로그인 유저의 recommended list

    # path('test/', get_login_user, name='us')  ##url에서 검색해서 되는지 확인하기
    path('testaddmovie/', users_views.test_add_mymovie, name='tam')  ##url에서 검색해서 되는지 확인하기

]