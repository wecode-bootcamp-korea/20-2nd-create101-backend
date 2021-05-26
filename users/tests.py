from django.test    import TestCase
from django.test    import Client
from unittest.mock  import patch, MagicMock

from users.models   import User, Coupon
from my_settings    import SECRET_KEY, ALGORITHM

class KakaoLoginTest(TestCase):
    def setUp(self):                        
        User.objects.create(
            kakao_id    = '1234567890',
            email       = 'shin91114@gmail.com',
            korean_name = '신승호'
        )
        
        Coupon.objects.create(
            name          = '신규회원',
            discount_rate = '30',
        )

        Coupon.objects.create(
            name          = '신규회원띠',
            discount_rate = '20',
        )

    def tearDown(self):                     
        User.objects.all().delete()

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
