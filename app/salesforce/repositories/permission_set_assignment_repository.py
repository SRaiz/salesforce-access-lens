from app.utils import Validation
from app.salesforce.domain import PermissionSetAssignment
from app.salesforce.repositories.base import BaseRepository
from app.salesforce.query import PermissionSetAssignmentQueries
from app.salesforce.mappers import PermissionSetAssignmentMapper

class PermissionSetAssignmentRepository( BaseRepository[ PermissionSetAssignment ] ):
    """
    Repository responsible for retrieving Permission Set Assignments.
    """

    def find_by_user_id( self, user_id: str ) -> list[ PermissionSetAssignment ]:
        """
        Finds all Permission Set Assignments for a Salesforce user.
        """

        Validation.validate_required( "user_id", user_id )

        response = self.query_executor.execute(
            query = PermissionSetAssignmentQueries.by_user_id( user_id )
        )

        records = response.get( "records", [] )
        return [
            PermissionSetAssignmentMapper.from_record( record )
            for record in records
        ]