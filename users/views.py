import json, jwt, requests
from datetime           import datetime


from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from decorator         import validate_login
from my_settings       import SECRET_KEY, ALGORITHM
from users.models      import User, Coupon, Like
from courses.models    import Course
from users.validations import validate_courses

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

class AddLikeView(View):
    @validate_login
    def post(self, request, course_id):
        try: 
            user   = request.account
            course = Course.objects.get(id=course_id)
            if course not in user.like.all():
                user.like.add(course) 
                return JsonResponse({'message' : 'ADD_COURSE_TO_LIKE'}, status=201)
                            
            else:
                Like.objects.filter(user_id=user, course_id=course).delete()
                return JsonResponse({'message' : 'DELETE_COURSE_FROM_LIKE'}, status=201)

        except Course.DoesNotExist:
            return JsonResponse({'message' : 'COURSE_NOT_EXIST'}, status=404)

class AddLookView(View):
    @validate_login
    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            user   = request.account
            user.look.add(course)  
            return JsonResponse({'message' : 'ADD_COURSE_TO_LOOK'}, status=201)

        except Course.DoesNotExist:
            return JsonResponse({'message' : 'COURSE_NOT_EXIST'}, status=404)

class UserView(View):
    @validate_login
    def get(self, request):
        user  = request.account
        user_info = {
            'name'  : user.korean_name,
            'email' : user.email,
            'coupon_list'   : [coupon_list.name for coupon_list in user.coupon.all()]
        }
        user_course = {
            'user_create_courses' : validate_courses(name='user_craete_course', user=user),
            'liked_courses'       : validate_courses(name='liked_course', user=user),
            'looked_courses'      : validate_courses(name='looked_course', user=user),
        }

        is_create_courses = user_course['user_create_courses'] != []
        is_liked_courses  = user_course['liked_courses'] != []
        is_looked_courses = user_course['looked_courses'] != []
        
        return JsonResponse({'message': 'SUCCESS', 'user_info' : user_info, 'user_course':user_course}, status=200)


        # message = {
        #     message1 : 'NOTHING',
        #     message2 : 'ONLY_LOOKED_COURSES',
        #     message3 : 'ONLY_LIKED_COURSES',
        #     message4 : 'ONLY_CREATED_COURSES',
        #     message5 : 'NO_CREATED_COURSES',
        #     message6 : 'NO_LIKED_COURSES',
        #     message7 : 'NO_LOOKED_COURSES'
        # }

        # if not is_create_courses and not is_liked_courses and not is_looked_courses:
        #     return JsonResponse({'message' : message[message1], 'user_info' : user_info, 'user_course':user_course}, status=200)

        # if not is_create_courses and not is_liked_courses:
        #     return JsonResponse({'message' : message[message2], 'user_info' : user_info, 'user_course':user_course}, status=200)
        # elif not is_create_courses and not is_looked_courses:
        #         return JsonResponse({'message' : message[message3], 'user_info' : user_info, 'user_course':user_course}, status=200)
        # elif not is_liked_courses and not is_looked_courses:
        #         return JsonResponse({'message' : message[message4], 'user_info' : user_info, 'user_course':user_course}, status=200)

        # if not is_create_courses:
        #     return JsonResponse({'message' : message[message5], 'user_course':user_course}, status=200)
        # elif not is_liked_courses:
        #     return JsonResponse({'message' : message[message6], 'user_info' : user_info, 'user_course':user_course}, status=200)
        # elif not is_looked_courses:
        #     return JsonResponse({'message' : message[message7], 'user_info' : user_info, 'user_course':user_course}, status=200)
        