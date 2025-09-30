from fastapi import HTTPException, status, Header
from config import settings


# Простая зависимость для проверки API ключа
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный API ключ",
        )
    return x_api_key
