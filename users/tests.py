import jwt
from datetime import datetime

from courses.models import Course, SubCategory
from django.test    import TestCase
from django.test    import Client
from unittest.mock  import patch, MagicMock

from courses.models import Category, SubCategory, Target
from users.models   import User, Coupon, Like, Look, UserCoupon
from my_settings    import SECRET_KEY, ALGORITHM

class KakaoLoginTest(TestCase):
    def setUp(self):
        category     = Category.objects.create(name='취미')
        sub_category = SubCategory.objects.create(name='스포츠', category_id = category.id)
        target       = Target.objects.create(name='중급자')                                
        
        user1 = User.objects.create(
            id          = 1,
            kakao_id    = '1234567890',
            email       = 'shin91114@gmail.com',
            korean_name = '신승호'
        )

        self.access_token1 = jwt.encode({
            'user_id': user1.id,
            'iat'    : datetime.now().timestamp()}, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )        

        user2 =  User.objects.create(
            id          = 2,
            kakao_id    = '0987654321',
            email       = 'user2@naver.com',
            korean_name = '강경훈'
        )

        self.access_token2 = jwt.encode({
            'user_id': user2.id,
            'iat'    : datetime.now().timestamp()}, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )        
        print(self.access_token2)
        user3 =  User.objects.create(
            id          = 3,
            kakao_id    = '0987654321',
            email       = 'user3@naver.com',
            korean_name = '홍연우'
        )

        self.access_token3 = jwt.encode({
            'user_id': user3.id,
            'iat'    : datetime.now().timestamp()}, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        ) 

        user4 =  User.objects.create(
            id          = 4,
            kakao_id    = '0987654321',
            email       = 'user4@naver.com',
            korean_name = '신따거'
        )

        self.access_token4 = jwt.encode({
            'user_id': user4.id,
            'iat'    : datetime.now().timestamp()}, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )        


        course1 = Course.objects.create(
            id = 1,
            description = '초급자분들을 위한 축구',
            thumbnail  = 'null.jpg',
            price = '30000.00',
            title = '축구계의 끝판왕',
            month = '6',
            sub_category_id = sub_category.id,
            target_id = target.id,
            user_id = user2.id
        )          

        course2 = Course.objects.create(
            id = 2,
            description = '중급자분들을 위한 축구',
            thumbnail  = 'null.jpg',
            price = '50000.00',
            title = '축구계의 끝판왕2',
            month = '12',
            sub_category_id = sub_category.id,
            target_id = target.id,
            user_id = user3.id
        )     

        course3 = Course.objects.create(
            id = 3,
            description = '고급자분들을 위한 축구',
            thumbnail  = 'null.jpg',
            price = '100000.00',
            title = '축구계의 끝판왕3',
            month = '18',
            sub_category_id = sub_category.id,
            target_id = target.id,
            user_id = user3.id
        )           
        
        Look.objects.create(
            user_id = user4.id,
            course_id = course2.id
        )

        Look.objects.create(
            user_id = user4.id,
            course_id = course3.id
        )
        Look.objects.create(
            user_id = user3.id,
            course_id = course2.id
        )  

        Look.objects.create(
            user_id = user3.id,
            course_id = course3.id
        )               
        # test_user_add_course_to_like 사용
        Like.objects.create(
            user_id = user4.id,
            course_id = course2.id
        )        
        # 
        Like.objects.create(
            user_id = user4.id,
            course_id = course3.id
        ) 

        Like.objects.create(
            user_id = user3.id,
            course_id = course2.id
        )   

        Like.objects.create(
            user_id = user3.id,
            course_id = course3.id
        )                   

        coupon1 = Coupon.objects.create(
            name = '신규회원',
            discount_rate = '30'
        )

        coupon2 = Coupon.objects.create(
            name = '10000할인 쿠폰',
            discount_rate = '10000'
        )        

        UserCoupon.objects.create(
            coupon_id = coupon1.id,
            user_id   = user2.id
        )

        UserCoupon.objects.create(
            coupon_id = coupon2.id,
            user_id   = user2.id
        )

    def tearDown(self):                     
        User.objects.all().delete()        
        Like.objects.all().delete()
        Look.objects.all().delete()
        Course.objects.all().delete()
 
# social login
    @patch("users.views.requests")
    def test_kakao_login_new_user_success_not_first_login(self, mocked_requests):  
        client = Client()                                           
        class MockedResponse:                                             
            def json(self):
                return {                                                   
                    "id"      : "1234567890",
                    "kakao_account" : { "email"   : "shin91114@gmail.com",
                                        'profile' : {'nickname' : '신승호'}
                                      }
                                    }

        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        headers             = {'HTTP_Authorization' : 'access_token'} 
        response            = client.post("/users/login/kakao", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.json().keys()),['message','Authorization'])        

    @patch("users.views.requests")                                 
    def test_kakao_login_new_user_success_coupons_for_new(self, mocked_requests):  
        client = Client()                                           
        class MockedResponse:                                             
            def json(self):
                return {                                                   
                    "id"      : "1234567891",
                    "kakao_account" : { "email"   : "shin91113@gmail.com",
                                        'profile' : {'nickname' : '신승구'}
                                      }
                                    }

        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        headers             = {'HTTP_Authorization' : 'access_token'} 
        response            = client.post("/users/login/kakao", **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(list(response.json().keys()),['message','Authorization'])

# courses lists user has
    def test_user_add_course_to_like_but_not_exist_course(self):
        client   = Client()
        headers  = {"HTTP_AUTHORIZATION": self.access_token2}
        response = client.post('/users/like/5', **headers)
        
        self.assertEqual(response.status_code, 404)  
        self.assertEqual(response.json()['message'], 'COURSE_NOT_EXIST')

    def test_user_info_and_no_liked_courses_no_looked_courses(self):  
        client   = Client()
        headers  = {"HTTP_AUTHORIZATION": self.access_token2}
        response = client.get('/users/me', **headers)

        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json()['message'],'NO_LIKED_COURSES_&_NO_LOOKED_COURSES')

    def test_user_info_and_no_create_courses_no_liked_courses_no_looked_courses(self):  
        client   = Client()
        headers  = {"HTTP_AUTHORIZATION": self.access_token1}
        response = client.get('/users/me', **headers)

        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json()['message'],'NO_CREATED_COURSES_&_NO_LIKED_COURSES_&_NO_LOOKED_COURSES')

    def test_user_info_and_no_create_courses(self):  
        client   = Client()
        headers  = {"HTTP_AUTHORIZATION": self.access_token4}
        response = client.get('/users/me', **headers)

        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json()['message'],'NO_CREATED_COURSES')        

#  add or delete course that user likes
    def test_user_add_course_to_like(self):  
            client   = Client()
            headers  = {"HTTP_AUTHORIZATION": self.access_token4}
            response = client.post('/users/like/1', **headers)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()['message'],'ADD_COURSE_TO_LIKE')        

    def test_user_delete_course_from_like(self):  
        client   = Client()
        headers  = {"HTTP_AUTHORIZATION": self.access_token4}
        response = client.post('/users/like/2', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'],'DELETE_COURSE_FROM_LIKE')

# add course that user looks
    def test_user_add_course_to_look(self):  
        client   = Client()
        headers  = {"HTTP_AUTHORIZATION": self.access_token4}
        response = client.post('/users/look/1', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'],'ADD_COURSE_TO_LOOK')          