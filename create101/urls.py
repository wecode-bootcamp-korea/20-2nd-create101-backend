from django.urls import include, path

urlpatterns = [
    path('courses', include('courses.urls')),
    path('users', include('users.urls')),
]