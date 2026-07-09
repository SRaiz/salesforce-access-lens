from app.utils import Validation
from app.salesforce.mappers import UserMapper
from app.salesforce.domain import SalesforceUser
from app.salesforce.query import SoqlQueryExecutor, UserQueries

class UserRepository:
    """
    Repository responsible for retrieving Salesforce users.
    """
    
    def __init__( self, query_executor: SoqlQueryExecutor ) -> None:
        self._query_executor    = query_executor
        
    @property
    def query_executor( self ) -> SoqlQueryExecutor:
        return self._query_executor
        
    def find_by_username( self, username: str ) -> SalesforceUser | None:
        """
        Finds a Salesforce user by username.
        """
        Validation.validate_required( "username", username )

        response = self._query_executor.execute(
            query = UserQueries.by_username( username )
        )
        
        record = self._get_first_record( response )
        if record is None:
            return None
        
        return UserMapper.from_record( record )
        
    def find_by_userid( self, user_id: str ) -> SalesforceUser | None:
        """
        Finds a Salesforce user by user Id.
        """
        Validation.validate_required( "user_id", user_id )
        
        response = self.query_executor.execute(
            query = UserQueries.by_id( user_id )
        )
        
        record = self._get_first_record( response )
        if record is None:
            return None
        
        return UserMapper.from_record( record )
        
    def find_by_email( self, email: str ) -> SalesforceUser | None:
        """
        Finds a Salesforce user by email.
        """
        Validation.validate_required( "email", email )
        
        response = self.query_executor.execute(
            query = UserQueries.by_email( email )
        )
        
        record = self._get_first_record( response )
        if record is None:
            return None
        
        return UserMapper.from_record( record )
    
    @staticmethod
    def _get_first_record( response: dict ) -> dict | None:
        records = response.get( "records", [] )
        
        if not records:
            return None
        
        return records[0]