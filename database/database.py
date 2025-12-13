from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Database:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close

    def create_table(self, base: type[DeclarativeBase]):
        base.metadata.create_all(bind=self.engine)


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/todo"
db_instance = Database(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass
