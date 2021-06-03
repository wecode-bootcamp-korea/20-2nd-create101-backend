from django.views          import View
from django.http           import JsonResponse
from django.db.models      import Count, Q
from django.core.paginator import Paginator, EmptyPage

from my_settings    import SECRET_KEY, ALGORITHM
from courses.utils  import get_user
from courses.models import Course, Category, SubCategory, Review
from users.models   import Like, Comment

class CategoryView(View):
    def get(self, request):
        results = [{
                'id'          : category.id,
                'name'        : category.name,
                'sub_category': [{
                    'id'  : sub_category.id,
                    'name': sub_category.name
                    }for sub_category in category.sub_categorys.all()]
             }for category in Category.objects.prefetch_related('sub_categorys').all()]
        return JsonResponse({'category': results}, status=200)

class CourseDetailView(View):
    def get(self, request, id):
        try:
            user            = get_user(request)
            course          = Course.objects.get(id=id)
            course_like     = Like.objects.filter(course_id=id)
            course_review   = Review.objects.filter(course_id=id)
            comments        = [question_id.id for question_id in course_review]
            review_comments = Comment.objects.filter(review_id__in=comments)
            course_info = {
                "id"            : course.id,
                "name"          : course.title,
                "price"         : course.price,
                "thumbnail" : str(course.thumbnail),
                "subcategory"   : course.sub_category.name,
                "counts_like"   : course_like.count(),
                "target"        : course.target.name,
                "month"         : course.month,
                'liked'         : user in course.liked_user.all(),
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
            
class CourseListView(View):
    def get(self, request):
        keyword           = request.GET.get('keyword', None)
        category_name     = request.GET.get('category', None)
        sub_category_name = request.GET.get('sub_category', None)
        user              = get_user(request)

        # 카테고리 분류
        if sub_category_name or category_name:
            if SubCategory.objects.filter(name=sub_category_name).exists() or Category.objects.filter(name=category_name).exists():
                course_list = Course.objects.select_related('sub_category','user').prefetch_related('liked_user').filter(
                    Q(sub_category__name           = sub_category_name) |
                    Q(sub_category__category__name = category_name))
            else:
                return JsonResponse({'message' : 'INVALID_VALUE'}, status=404)
        else:
            course_list = Course.objects.select_related('sub_category','user').prefetch_related('liked_user').all()
        
        # 검색 기능
        if keyword:
            course_list = Course.objects.select_related('sub_category', 'user').prefetch_related('liked_user').filter(
                Q(title__icontains = keyword) |
                Q(sub_category__name__icontains = keyword) |
                Q(sub_category__category__name__icontains = keyword) 
            )

        # 정렬
        course_list = course_list.annotate(like_count = Count('liked_user'), review_count = Count('course_review'))
        sort_name   = request.GET.get('sort', None)
        if sort_name:
            my_dict = {
                'lastest'  : '-created_at',
                'reviewest': '-review_count',
                'likes'    : '-like_count'
            }
            if sort_name in my_dict.keys():
                ordered_course_list = course_list.order_by(my_dict[sort_name])
                course_list         = ordered_course_list
            else:
                return JsonResponse({'message' : 'INVALID_VALUE'}, status=404)
        
        # pagination
        page      = request.GET.get('page', None)
        page_list = []
        if page:
            PAGE_SIZE = 10
            paginator = Paginator(course_list, PAGE_SIZE)
            try:
                list_by_page = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'message' : 'INVALID_PAGE'}, status=404)
            course_list = list_by_page.object_list
            page_list   = [page for page in paginator.page_range]

        results = [
            {
                'id'          : course.id,
                'title'       : course.title,
                'sub_category': course.sub_category.name,
                'user'        : course.user.korean_name,
                'like'        : course.like_count,
                'price'       : int(course.price),
                'thumbnail'   : str(course.thumbnail),
                'month'       : course.month,
                'liked'       : user in course.liked_user.all()
            }
        for course in course_list]
        
        return JsonResponse({'courses':results, 'page_list':page_list}, status=200)