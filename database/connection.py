# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

## DATABASE_URL = "postgresql://user:password@host:port/database"
## Используем URL из настроек
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


engine = create_engine(
    "postgresql+psycopg2://myuser:mypassword@172.17.0.2:5432/mydatabase"
)


# Создаем SessionLocal класс, который будет использоваться для создания сессий базы данных
# autocommit=False: Мы будем явно коммитить изменения.
# autoflush=False: Мы не будем сбрасывать изменения в базу данных после каждого запроса, чтобы избежать ненужных операций.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
