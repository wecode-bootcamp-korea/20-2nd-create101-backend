from django.urls    import path

from courses.views  import CourseDetailView, CategoryView, CourseListView, CourseRegisterView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/<int:id>', CourseDetailView.as_view()),
    path('/register', CourseRegisterView.as_view())
]

