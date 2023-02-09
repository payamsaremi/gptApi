import jwt
from fastapi import HTTPException

# def create_jwt(payload: dict, secret: str, algorithm: str = 'HS256'):
#     try:
#         return jwt.encode(payload, secret, algorithm=algorithm).decode('utf-8')
#     except Exception as e:
#         raise HTTPException(status_code=500, detail='Error creating JWT: {}'.format(str(e)))

def validate_jwt(jwt_token: str, secret: str, algorithms: list):
      try:
        return jwt.decode(jwt_token, secret, algorithms=algorithms)
      except:
        raise HTTPException(status_code=400, detail='Error decoding JWT {}'.format(jwt_token))