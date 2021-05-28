import json

from django.test     import TestCase, Client

from courses.models  import Category, SubCategory, Course, Review, Target
from users.models    import Like, Comment, User
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
                "thumbnail_url" : "abcd.jpg",
                "subcategory"   : "미술",
                "counts_like"   : 1,
                "target"        : "초급자용",
                "month"         : 6,
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
