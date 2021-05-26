from django.urls import path

from courses.views import CategoryView
urlpatterns = [
    path('/category', CategoryView.as_view())
]