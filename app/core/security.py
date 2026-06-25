from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password[:72])


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password[:72],
        hashed_password
    )


def create_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=24
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def decode_token(token):

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except:
        return None