from app.salesforce.domain import ObjectPermission
from app.salesforce.mappers import ObjectPermissionMapper
from app.salesforce.query import ObjectPermissionQueries
from app.salesforce.repositories.base import BaseRepository
from app.utils import Validation


class ObjectPermissionRepository(BaseRepository):
    """
    Repository responsible for retrieving Salesforce object permissions.
    """

    def find_by_parent_id( self, parent_id: str ) -> list[ ObjectPermission ]:
        """
        Finds all object permissions belonging to one Permission Set.
        """

        Validation.validate_required( "parent_id", parent_id )

        response = self.query_executor.execute(
            query = ObjectPermissionQueries.by_parent_id( parent_id )
        )

        records = response.get("records", [])

        return [
            ObjectPermissionMapper.from_record( record )
            for record in records
        ]

    def find_by_parent_ids( self, parent_ids: set[str] ) -> list[ ObjectPermission ]:
        """
        Finds all object permissions belonging to multiple Permission Sets.
        """

        if not parent_ids:
            return []

        response = self.query_executor.execute(
            query = ObjectPermissionQueries.by_parent_ids( parent_ids )
        )

        records = response.get("records", [])

        return [
            ObjectPermissionMapper.from_record( record )
            for record in records
        ]