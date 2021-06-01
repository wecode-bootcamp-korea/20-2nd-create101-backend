import jwt

from users.models import User

from my_settings import SECRET_KEY, ALGORITHM

def get_user(request):
    access_token = request.headers.get("Authorization")
    if access_token:
        token_payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return User.objects.get(id=token_payload['user_id'])
    else: return None