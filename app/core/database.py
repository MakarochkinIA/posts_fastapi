from pathlib import Path
from sqlmodel import Session, create_engine, select
import os

from app import crud
from app.core.config import settings
from app.models.users import User, UserCreate


DB_PATH = str((Path() / 'app' / 'db.sqlite').resolve())
sqlite_file_name = "db.sqlite"
sqlite_url = f'sqlite:///{DB_PATH}'
connect_args = {"check_same_thread": False}
SQLALCHEMY_DATABASE_URL = os.getenv(
    'DB_CONN',
    sqlite_url
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args=connect_args
)


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported
    # and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
