import datetime

import jwt
from blog.settings import SECRET_JWT


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1440)
    }
    access_token = jwt.encode(access_token_payload,
                              SECRET_JWT, algorithm='HS256').decode('utf-8')
    return access_token
