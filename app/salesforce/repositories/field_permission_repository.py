from app.salesforce.domain import FieldPermission
from app.salesforce.mappers import FieldPermissionMapper
from app.salesforce.query import FieldPermissionQueries
from app.salesforce.repositories.base import BaseRepository
from app.utils import Validation


class FieldPermissionRepository(BaseRepository):
    """
    Repository responsible for retrieving Salesforce field permissions.
    """

    def find_by_parent_id( self, parent_id: str ) -> list[ FieldPermission ]:
        """
        Finds all field permissions belonging to one Permission Set.
        """

        Validation.validate_required( "parent_id", parent_id )

        response = self.query_executor.execute(
            query = FieldPermissionQueries.by_parent_id( parent_id )
        )

        records = response.get( "records", [] )

        return [
            FieldPermissionMapper.from_record( record )
            for record in records
        ]

    def find_by_parent_ids( self, parent_ids: set[ str ] ) -> list[ FieldPermission ]:
        """
        Finds all field permissions belonging to multiple Permission Sets.
        """

        if not parent_ids:
            return []

        response = self.query_executor.execute(
            query = FieldPermissionQueries.by_parent_ids( parent_ids )
        )

        records = response.get( "records", [] )

        return [
            FieldPermissionMapper.from_record( record )
            for record in records
        ]