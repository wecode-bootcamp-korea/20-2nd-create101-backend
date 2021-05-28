from django.urls    import path
from courses.views  import CourseDetailView, CategoryView


urlpatterns = [
    path('/<int:id>', CourseDetailView.as_view()),
    path('/category', CategoryView.as_view())
]
