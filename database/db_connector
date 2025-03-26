import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DBConnector:
    def __init__(self, db_type='sqlite'):
        """
        Initialize database connection
        :param db_type: 'sqlite' or 'postgresql'
        """
        self.db_type = db_type
        self.engine = None
        self.Session = None
        self._setup_engine()

    def _setup_engine(self):
        """Configure database engine based on type"""
        if self.db_type == 'sqlite':
            db_path = os.getenv('SQLITE_DB_PATH', 'database/sems.db')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.engine = create_engine(f'sqlite:///{db_path}', pool_pre_ping=True)
        elif self.db_type == 'postgresql':
            self.engine = create_engine(
                f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
                f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}",
                pool_size=20,
                max_overflow=30
            )
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

        self.Session = scoped_session(
            sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
        )

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around database operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_tables(self, base):
        """Create all tables from SQLAlchemy models"""
        try:
            base.metadata.create_all(self.engine)
            print("Tables created successfully")
        except SQLAlchemyError as e:
            print(f"Error creating tables: {e}")

# Singleton instance
db = DBConnector(os.getenv('DB_TYPE', 'sqlite'))

# Example usage:
if __name__ == '__main__':
    from database.models import Base  # Import your models
    db.create_tables(Base)
