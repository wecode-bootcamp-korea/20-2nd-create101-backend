import jwt
from datetime     import datetime

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

def validate_login(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            if not access_token:
                return JsonResponse({'message': 'LOGIN_REQUIRED'}, status=401)

            token_payload = jwt.decode(
                    access_token,
                    SECRET_KEY,
                    algorithms=ALGORITHM
            )

            expiration_delta = 60000000
            now = datetime.now().timestamp()                   
            if now > token_payload['iat'] + expiration_delta:  
                return JsonResponse({'message': 'TOKEN_EXPIRED'}, status=401)

            request.account = User.objects.get(id=token_payload['user_id']) 
            return func(self, request, *args, **kwargs)
            
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_JWT'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
    return wrapper