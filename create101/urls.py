from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('course', include('course.urls'))
]
