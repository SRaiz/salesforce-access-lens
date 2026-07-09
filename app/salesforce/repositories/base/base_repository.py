from typing import Generic, TypeVar
from app.salesforce.query import SoqlQueryExecutor

T = TypeVar( "T" )

class BaseRepository( Generic[T] ):
    """
    Base class for Salesforce repositories.
    """

    def __init__( self, query_executor: SoqlQueryExecutor ) -> None:
        self._query_executor = query_executor

    @property
    def query_executor( self ) -> SoqlQueryExecutor:
        return self._query_executor

    @staticmethod
    def _get_first_record( response: dict ) -> dict | None:
        records = response.get( "records", [] )

        if not records:
            return None

        return records[0]