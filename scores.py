import pandas as pd
from os.path import join
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SW2019test1_.settings')
django.setup()
scores_data = []

from users.models import Score
#
# ## Score 안에 있는 객체 모두 삭제
# queryset = Score.objects.all()
# queryset.delete()

# 사용자별 평점수 기준에 따라 삭제한 데이터 가져오기
# for i in range(1, 64):
#     scores_data.append(pd.read_csv(join('C:\\','Users','yousu', 'Documents', 'DataScience', 'SW201909','edit_users_scores1114~', 'edit_users_scores'+str(i)+'.csv'), encoding='utf-8'))

for i in range(63):
    scores_data.append(pd.read_csv(
        join('C:\\', 'Users', 'yousu', 'Documents', 'DataScience', 'SW201909', 'edit_users_scores1119',
             'edit1119_scores' + str(i) + '.csv'), encoding='utf-8'))
# 영화 평점수 다 합치기
total_scores = pd.concat(scores_data)
total_scores = total_scores.reset_index(drop=True)
total_scores.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
# 영화 평점들 데이터 제목순으로 정렬
total_scores = total_scores.sort_values('movie_title')
total_scores.drop(['Unnamed: 0.1.1'], axis=1, inplace=True)
total_scores = total_scores.reset_index(drop=True)
# total_scores.drop(['index'], axis=1, inplace=True)

scores = []

for index, row in total_scores[4783759:].iterrows():
    print(index)
    tuple = (row['movie_title'], row['nickname'], row['score'])
    scores.append(tuple)

# instances = []
index1 = 4783758
for (title, nickname, score) in scores:
    #instances.append(Score(title=title, nickname=nickname, score=score))
    Score.objects.create(title=title, nickname=nickname, score=score)
    index1 += 1
    print('#', index1, title, nickname, score)

# Score.objects.bulk_create(instances)
