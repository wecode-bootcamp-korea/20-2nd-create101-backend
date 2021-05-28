from django.http.response   import JsonResponse
from django.views           import View

from courses.models         import Course, Review, Category
from users.models           import User, Like, Comment

class CategoryView(View):
    def get(self, request):
        results = [{
                'id'          : category.id,
                'name'        : category.name,
                'sub_category': [{
                    'id'  : sub_category.id,
                    'name': sub_category.name
                    }for sub_category in category.sub_categorys.all()]
             }for category in Category.objects.all()]
        return JsonResponse({'category': results}, status=200)

class CourseDetailView(View):
    def get(self, request, id):
        try:
            course          = Course.objects.get(id=id)
            course_like     = Like.objects.filter(course_id=id)
            course_review   = Review.objects.filter(course_id=id)
            comments        = [question_id.id for question_id in course_review]
            review_comments = Comment.objects.filter(review_id__in=comments)
            course_info = {
                "id"            : course.id,
                "name"          : course.title,
                "price"         : course.price,
                "thumbnail_url" : course.thumbnail,
                "subcategory"   : course.sub_category.name,
                "counts_like"   : course_like.count(),
                "target"        : course.target.name,
                "month"         : course.month,
                "review"        : [{
                    'id'     : review.id,
                    'text'   : review.text,
                    'user_id': review.user_id
                } for review in course_review],
                "comment"       : [{
                    'text'       : comment.text,
                    'user_id'  : comment.user_id,
                    'review_id': comment.review_id
                } for comment in review_comments] 
            }        
            return JsonResponse({'status': "SUCCESS", 'data': {'course':course_info}}, status=200)
        except Course.DoesNotExist:
            return JsonResponse({"status": "COURSE_NOT_FOUND", "message": "존재하지 않는 클래스입니다."}, status=404)
