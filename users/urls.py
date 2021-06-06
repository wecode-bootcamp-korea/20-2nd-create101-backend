from django.urls import path

from users.views  import KakaologinView, UserView, AddLikeView, AddLookView

urlpatterns = [
    path('/login/kakao', KakaologinView.as_view()),
    path('/me', UserView.as_view()),
    path('/like/<int:course_id>', AddLikeView.as_view()),
    path('/look/<int:course_id>', AddLookView.as_view()),
]

