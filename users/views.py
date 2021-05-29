import jwt, requests

from django.http      import JsonResponse
from django.views     import View

from datetime         import datetime
from my_settings      import SECRET_KEY, ALGORITHM
from users.models     import User, Coupon

class KakaologinView(View):
    def post(self, request):
        try:
            access_token   = request.headers.get("Authorization", None)       

            token_info_url = 'https://kapi.kakao.com/v2/user/me'              
            headers        = {'Authorization' : f"Bearer {access_token}"}     

            user_info_response = requests.post(token_info_url, headers=headers) 
            user_info_json     = user_info_response.json()                      

            kakao_account      = user_info_json.get('kakao_account')            
            kakao_id           = user_info_json.get('id')   

            user, first_login = User.objects.get_or_create(            
                    kakao_id    = kakao_id,
                    email       = kakao_account['email'],
                    korean_name = kakao_account['profile']['nickname'], 
                )
            
            access_token = jwt.encode(
                        {'user_id': user.id,
                            'iat' : datetime.now().timestamp()
                        }, 
                        SECRET_KEY, 
                        algorithm = ALGORITHM
                        )

            coupons    = Coupon.objects.filter(name__contains = "신규회원")
            if first_login:
                user.coupon.add(*coupons)       # 신규 가입자에게 "신규회원" 쿠폰 증정예정
                return JsonResponse({'message' : 'SUCCESS', 'Authorization' : access_token}, status=201)
            else:
                 return JsonResponse({'message' : 'SUCCESS', 'Authorization' : access_token}, status=200)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=200)