from django.urls import path

from users.views  import KakaologinView

urlpatterns = [
    path('/login/kakao', KakaologinView.as_view()),
]

