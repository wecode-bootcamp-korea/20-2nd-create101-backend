from django.urls    import path

from courses.views  import CourseDetailView, CategoryView, CourseListView, CourseRegisterView

from courses.views import CategoryView, CourseReviewView, CourseCommentView
urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/review/<int:course_id>', CourseReviewView.as_view()),
    path('/comment/<int:review_id>', CourseCommentView.as_view())
]
