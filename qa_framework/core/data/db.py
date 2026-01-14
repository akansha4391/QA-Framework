from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from qa_framework.core.config import settings
from qa_framework.core.logger import get_logger
from qa_framework.core.exceptions import DataLoadingError

logger = get_logger("db_manager")

class DBManager:
    """
    Database Manager using SQLAlchemy.
    """
    def __init__(self, connection_string: str = None):
        if not connection_string:
            connection_string = settings.DB_CONNECTION_STRING
        
        if not connection_string:
             logger.warning("No DB connection string provided in settings.")
             self.engine = None
             self.Session = None
             return

        try:
            self.engine = create_engine(connection_string)
            self.Session = scoped_session(sessionmaker(bind=self.engine))
        except Exception as e:
            raise DataLoadingError("Failed to initialize DB Connection", e)

    def execute_query(self, query: str, params: dict = None):
        """Executes a raw SQL query."""
        if not self.Session:
            raise DataLoadingError("DB Not initialized")
        
        session = self.Session()
        try:
            result = session.execute(text(query), params or {})
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise DataLoadingError(f"Query execution failed: {query}", e)
        finally:
            session.close()

    def fetch_all(self, query: str, params: dict = None):
        """Fetches all results from a query."""
        if not self.Session:
            raise DataLoadingError("DB Not initialized")

        session = self.Session()
        try:
            result = session.execute(text(query), params or {})
            return result.fetchall()
        finally:
            session.close()
