from django.contrib import admin

# 관리자 페이지에서 users 앱 모델 관리 가능하도록
from users.models import UserInfo, Movie, Score, UserMovie, RecommendedMovie

admin.site.register(UserInfo)
admin.site.register(Movie)
admin.site.register(Score)
admin.site.register(UserMovie)
admin.site.register(RecommendedMovie)
