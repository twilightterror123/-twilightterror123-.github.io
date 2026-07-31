from passlib.context import CryptContext
from sqlalchemy import select
from core.database import async_session
from models.user import User
import jwt
from datetime import datetime, timedelta
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    async def authenticate(username: str, password: str):
        async with async_session() as db:
            result = await db.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()
            if not user:
                return None
            if not pwd_context.verify(password, user.hashed_password):
                return None
            return user

    @staticmethod
    def create_access_token(user_id: str):
        exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode({"sub": user_id, "exp": exp}, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def create_refresh_token(user_id: str):
        exp = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        return jwt.encode({"sub": user_id, "exp": exp}, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_refresh_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload["sub"]
        except:
            return None
