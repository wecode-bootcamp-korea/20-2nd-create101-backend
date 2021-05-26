from django.views import View
from django.http  import JsonResponse

from courses.models import Category

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
