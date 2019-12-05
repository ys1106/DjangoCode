import os
import django
# import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SW2019test1_.settings')
django.setup()
from users.models import Score
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
# from os.path import join

# from numpy import dot
# from numpy.linalg import norm

# import dask.dataframe as dd
# import dask.array as da
#
# 평점 DB에서 가져오기
total_scores = list(Score.objects.all().values())
total_scores = pd.DataFrame(total_scores)  # ???
total_scores.sort_values('title', inplace=True)
total_scores.reset_index(drop=True, inplace=True)
print('total_scores', total_scores)  # total_scores에서 id 삭제해야??
total_scores

#
# # 현재 로그인 되어있는 사용자 닉네임?
# def get_login_user(request):
#
#     return HttpResponse(str(request.user.username))
# user_id = get_login_user()

#

################ db에서 가져와지는지 확인 ##################
# movie_info = list(Movie.objects.all().values())
# movie_info
# df_movie_info = pd.DataFrame(movie_info)
# df_movie_info
# df_movie_info.sort_values('title').reset_index()
##########################################################
# # db 넣기 전_파일로 데이터 가져오기
# scores_data = []
# for i in range(63):
#     scores_data.append(pd.read_csv(
#         join('C:\\', 'Users', 'yousu', 'Documents', 'DataScience', 'SW201909', 'edit_users_scores1119',
#              'edit1119_scores' + str(i) + '.csv'), encoding='utf-8'))
# 영화 평점수 다 합치기
# total_scores = pd.concat(scores_data).drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], axis=1)
# total_scores.reset_index(drop=True, inplace=True)
# # 영화 평점들 데이터 제목순으로 정렬
# total_scores.sort_values('movie_title').reset_index(drop=True, inplace=True)
# total_scores

## pivot -> groupby
groupby_scores = total_scores.groupby(['nickname', 'title'])['score'].max().unstack()
groupby_scores.fillna(0, inplace=True)
# groupby_scores.dtypes
# groupby_scores = groupby_scores.astype('int64')
groupby_scores = groupby_scores.astype('float32')
# groupby_scores.dtypes
print('groupby_scores', groupby_scores)
groupby_scores.to_csv('groupby_scores.csv', encoding='utf-8-sig')


# index -movie title / score열- 0인 df 만들어서 csv저장 (예측행렬 구할 때 쓰임)
scores_for_user = pd.DataFrame(data=np.zeros(groupby_scores.shape[1]), index=groupby_scores.columns, columns=['score'])
scores_for_user.to_csv('scores_for_user.csv', index=True, encoding='utf-8-sig')


groupby_scores.columns
# 코사인 유사도
groupby_score_T = groupby_scores.transpose()
cos_array = cosine_similarity(groupby_score_T, groupby_score_T)
cos_matrix = pd.DataFrame(data=cos_array, index=groupby_scores.columns, columns=groupby_scores.columns)
cos_matrix.to_csv('cos_matrix.csv', encoding='utf-8-sig')

# def predict_scores_one(score_series, cos_arr, num):  # 사용자 한 명에 대한 예측평점 행렬 구하기
#     score_arr = score_series.values
#
#     predict_matrix = pd.DataFrame(np.zeros(score_arr.shape), index=score_series.index)
#     predict_matrix = predict_matrix.astype('float32')
#
#     for ind in range(score_arr.shape[0]):
#         # top_n = np.array(np.array(cos_matrix.iloc[:, col]).argsort()[-2:-num - 2:-1]) ## 자기자신을 제외하기 위해 인덱싱 변경??? (자기자신과의 유사도가 1이니까)
#         top_n = np.argsort(cos_arr[:, ind])[:-num - 1:-1]
#
#         print(ind)
#         predict_matrix.iloc[ind] = cos_arr[ind, :][top_n].dot(np.transpose(score_arr[top_n]))
#         predict_matrix.iloc[ind] /= np.sum(np.abs(cos_arr[ind, :][top_n]))
#
#         predict_matrix.to_csv('cosine_matrix_one'+'nickname'+'.csv', encoding='utf-8-sig')
#     return predict_matrix
#
#
# def get_unseen_movies(scores_matrix, userid):  # 사용자가 보지 않은 영화 리스트 가져오기
#     user_rating = scores_matrix.loc[userid, :]
#
#     already_seen = user_rating[user_rating > 0].index.tolist()
#
#     movie_list = scores_matrix.columns.tolist() # 모든 영화명
#
#     unseen_list = [movie for movie in movie_list if movie not in already_seen]
#
#     return unseen_list
#
#
# def recom_movies_one_user(predict_matrix_one_user, unseen_list_one_user, topn):  # 영화 추천_예측평점 행렬에서 topn개 가져오기
#     recom_movies = predict_matrix_one_user.loc[unseen_list_one_user].sort_values([0], ascending=False)[:topn]
#     return recom_movies


# cos_matrix['토이 스토리'].sort_values(ascending=False)
#
# # pred_matrix_one_user = predict_scores_one(groupby_scores.iloc[1541], cos_matrix.values, 20)
# pred_matrix_user = predict_scores_one(groupby_scores.loc[login_id], cos_matrix.values, num=20)
#
# # ex_userid = groupby_scores.iloc[1541].name
# # ex_unseen_list = get_unseen_movies(groupby_scores, ex_userid)
# unseen_list_user = get_unseen_movies(groupby_scores, login_id)
#
# # ex_recom_movies = recom_movies_one_user(pred_matrix_one_user, ex_unseen_list, topn=5)
# recom_movies_user = recom_movies_one_user(pred_matrix_user, unseen_list_user, topn=5)
#
# # 추천된 영화리스트 RecommendedMovie DB에 넣기
# try: # 현재 로그인 되어있는 사용자 RecommendedMovie 객체 가져옴
#     user_recom = RecommendedMovie.objects.get(user=request.user)
# except:  # ???
#     pass
# for movie in recom_movies_user:
#     try:
#         recom_movie = Movie.objects.get(title=movie) # 영화 객체 가져옴
#     except:
#         recom_movie = Movie.objects.create(title=movie) # 없으면 생성하는데, 이거 실행되면 안됨
#         recom_movie.save()  # ???????
#     # 그 영화 객체를 이 유저의 추천리스트에 추가
#     try: # 이미 그 영화가 추천리스트에 있으면
#         user_recom.recommend_list.get(recom_movie)
#     except:
#         user_recom.recommend_list.add(recom_movie)

#
#
# def predict_scores(score_matrix, cos_arr, num):  # 예측평점 행렬 구하기
#     score_arr = score_matrix.values
#
#     predict_matrix = pd.DataFrame(np.zeros(score_arr.shape), index=score_matrix.index, columns=score_matrix.columns)
#     predict_matrix = predict_matrix.astype('float32')
#
#     for col in range(score_arr.shape[1]):
#         # top_n = np.array(np.array(cos_matrix.iloc[:, col]).argsort()[-2:-num - 2:-1]) ## 자기자신을 제외하기 위해 인덱싱 변경??? (자기자신과의 유사도가 1이니까)
#         top_n = np.argsort(cos_arr[:, col])[:-num - 1:-1]
#
#         for row in range(score_arr.shape[0]):
#             print(col, '--', row)
#             predict_matrix.iloc[row, col] = cos_arr[col, :][top_n].dot(np.transpose(score_arr[row, :][top_n]))
#             predict_matrix.iloc[row, col] /= np.sum(np.abs(cos_arr[col, :][top_n]))
#
#         predict_matrix.to_csv('cosine_matrix.csv', encoding='utf-8-sig')
#     return predict_matrix
#
#
#
# # 테스트
# pred_matrix = predict_scores(groupby_scores, cos_matrix.values, num=20)
# # 사용자 한 명 테스트
#
#
#
# def recom_movies_userid(predict_matrix, userid, unseen_list, topn):  # 영화 추천_예측평점 행렬에서 topn개 가져오기
#     recom_movies = predict_matrix.loc[userid, unseen_list].sort_values(ascending=False)[:topn]
#     return recom_movies
