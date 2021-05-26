from django.test import TestCase, Client
from courses.models import Category, SubCategory

class CategoryTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
                id   = 1,
                name = 'test_category1'
            )
        
        SubCategory.objects.create(
            id       = 1,
            name     = 'test_sub_category1',
            category = category
        )
        SubCategory.objects.create(
            id       = 2,
            name     = 'test_sub_category2',
            category = category
        )
        

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
       
    def test_category_get_view(self):
        client   = Client()
        response = client.get('/courses/category')
        self.assertEqual(response.json(), {
            'category': [
                {
                    'id'          : 1,
                    'name'        : 'test_category1',
                    'sub_category': [
                            {
                            'id'  : 1,
                            'name': 'test_sub_category1'
                            },
                            {
                            'id'  : 2,
                            'name': 'test_sub_category2'
                            }
                        ]
                }
            ]
        })
        self.assertEqual(response.status_code, 200)


