import json

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from courses.models                 import Category, SubCategory, Course, Review, Target
from users.models                   import Like, Comment, User
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
        
class CourseDetailViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            email       = "abc@naver.com",
            korean_name = "철수",
            password    = "12345",
            kakao_id    = 1
        )
        Category.objects.create(
            id   = 1,
            name = "강의"
        )
        SubCategory.objects.create(
            id          = 1,
            name        = "미술",
            category_id = 1
        )
        Target.objects.create(
            id   = 1,
            name = "초급자용"
        )
        Course.objects.create(
            id              = 1,
            title           = "드로잉",
            price           = 240000,
            description     = "abcd",
            thumbnail       = "abcd.jpg",
            month           = 6,
            sub_category_id = 1,
            target_id       = 1,
            user_id         = 1
        )
        Like.objects.create(
            id        = 1,
            course_id = 1,
            user_id   = 1
        )
        Review.objects.create(
            id        = 1,
            text      = "hihi",
            course_id = 1,
            user_id   = 1
        )
        Comment.objects.create(
            id        = 1,
            user_id   = 1,
            review_id = 1,
            text      = "hello"
        )
    
    def tearDown(self):
        Course.objects.all().delete()

    def test_CourseDetailView_get_success(self):
        client          = Client()
        response        = client.get('/courses/1')

        self.assertEqual(response.json(),
            {'status': "SUCCESS", 'data': {'course': {
                "id"            : 1,
                "name"          : "드로잉",
                "price"         : "240000.00",
                "thumbnail"     : "abcd.jpg",
                "subcategory"   : "미술",
                "counts_like"   : 1,
                "target"        : "초급자용",
                "month"         : 6,
                "liked"         : False,
                "review"        : [{
                    'id'     : 1,
                    'text'   : "hihi",
                    'user_id': 1
                }],
                "comment"       : [{
                    'text'       : "hello",
                    'user_id'  : 1,
                    'review_id': 1,
                }]}}}    
        )
        self.assertEqual(response.status_code, 200)

    def test_CourseDetailView_DoesNotExist(self):
        client          = Client()
        response        = client.get('/courses/999')

        self.assertEqual(response.json(),
            {"status": "COURSE_NOT_FOUND", "message": "존재하지 않는 클래스입니다."}
        )
        self.assertEqual(response.status_code, 404)


class CourseListViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            email       = 'user1@wecode.com',
            korean_name = 'user1'
        )
        Category.objects.create(id=1, name='category1')
        category = Category.objects.create(id=2, name='category2')
        SubCategory.objects.create(
            id       = 1,
            name     = 'sub_category1',
            category = category)
        SubCategory.objects.create(
            id       = 2,
            name     = 'sub_category2',
            category = category)
        Target.objects.create(
            id   = 1,
            name = 'target1'
        )
        Course.objects.create(
            id           = 1,
            title        = 'course1',
            sub_category = SubCategory.objects.get(id=1),
            user         = User.objects.get(id=1),
            price        = 1.00,
            thumbnail    = 'null',
            month        = 1,
            description  = 'description',
            target       = Target.objects.get(id=1)
        )
        Course.objects.create(
            id           = 2,
            title        = 'course2',
            sub_category = SubCategory.objects.get(id=2),
            user         = User.objects.get(id=1),
            price        = 1.00,
            thumbnail    = 'null',
            month        = 1,
            description  = 'description',
            target       = Target.objects.get(id=1)
        )
        Review.objects.create(
            course = Course.objects.get(id=2),
            user   = User.objects.get(id=1),
            text   = 'review'
        )
        Like.objects.create(
            course = Course.objects.get(id=2),
            user   = User.objects.get(id=1)
        )
    
    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Target.objects.all().delete()
        Review.objects.all().delete()
        Like.objects.all().delete()
        User.objects.all().delete()

    def test_list_by_category_success(self):
        client   = Client()
        response = client.get('/courses?category=category2')
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json(), {
            'courses': [
                    {
                        'id'          : 1,
                        'title'       : 'course1',
                        'sub_category': 'sub_category1',
                        'user'        : 'user1',
                        'like'        : 0,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    },
                    {
                        'id'          : 2,
                        'title'       : 'course2',
                        'sub_category': 'sub_category2',
                        'user'        : 'user1',
                        'like'        : 1,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    }],
                'page_list': []
        })

    def test_list_by_category_invalid_value(self):
        client   = Client()
        response = client.get('/courses?category=category3')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'message' : 'INVALID_VALUE'
        })

    def test_list_by_sub_category_success(self):
        client   = Client()
        response = client.get('/courses?sub_category=sub_category2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'courses': [
                    {
                        'id'          : 2,
                        'title'       : 'course2',
                        'sub_category': 'sub_category2',
                        'user'        : 'user1',
                        'like'        : 1,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    }],
                'page_list': []
        })

    def test_list_by_sub_category_invalid_value(self):
        client   = Client()
        response = client.get('/courses?sub_category=sub_category3')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'message' : 'INVALID_VALUE'
        })
        

    def test_sorted_list_success(self):
        client     = Client()
        response   = client.get('/courses?sort=likes')
        self.assertEqual(response.json(), {
            'courses': [
                    {
                        'id'          : 2,
                        'title'       : 'course2',
                        'sub_category': 'sub_category2',
                        'user'        : 'user1',
                        'like'        : 1,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    },
                    {
                        'id'          : 1,
                        'title'       : 'course1',
                        'sub_category': 'sub_category1',
                        'user'        : 'user1',
                        'like'        : 0,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    }],
                'page_list': []
        })
        self.assertEqual(response.status_code, 200)
    
    def test_sorted_list_invalid_value(self):
        client   = Client()
        response = client.get('/courses?sort=invalid')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'message' : 'INVALID_VALUE'
        })

    def test_pagination_success(self):
        client   = Client()
        response = client.get('/courses?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'courses': [
                    {
                        'id'          : 1,
                        'title'       : 'course1',
                        'sub_category': 'sub_category1',
                        'user'        : 'user1',
                        'like'        : 0,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    },
                    {
                        'id'          : 2,
                        'title'       : 'course2',
                        'sub_category': 'sub_category2',
                        'user'        : 'user1',
                        'like'        : 1,
                        'price'       : 1,
                        'thumbnail'   : 'null',
                        'month'       : 1,
                        'liked'       : False,
                    }],
                'page_list': [1]
        })

    def test_pagination_invalid_value(self):
        client = Client()
        response = client.get('/courses?page=2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {'message' : 'INVALID_PAGE'}
        )
class CourseRegisterViewTest(TestCase):
    def setUp(self):
        User.objects.create(
                id          = 1,
                email       = "abc@naver.com",
                korean_name = "철수",
                password    = "12345678",
                kakao_id    = 1
            )

    def tearDown(self):
        User.objects.all().delete()

    def test_course_register_view_post_success(self):
        image = SimpleUploadedFile(name="test.png", content_type="image/png", content="")
        image_url = image.name
        client = Client()
        course = {
            'title': "드로잉수업2",
            'price': 30000,
            'thumbnail': image_url,
            'month': 3,
            'target': 1,
            'sub_category': 1,
            'user': 1
        }
        response = client.post('/courses/register', json.dumps(course), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_course_register_view_invalid_keys(self):
        image = SimpleUploadedFile(name="test.png", content_type="image/png", content="")
        image_url = image.name
        client = Client()
        course = {
            'title_name': "드로잉수업2",
            'price': 30000,
            'thumbnail': image_url,
            'month': 3,
            'target': 1,
            'sub_category': 1,
            'user': 1
        }
        response = client.post('/courses/register', json.dumps(course), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_KEYS"})
