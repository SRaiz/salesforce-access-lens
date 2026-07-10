from app.salesforce.domain import PermissionSet
from app.salesforce.mappers import PermissionSetMapper
from app.salesforce.query import PermissionSetQueries
from app.salesforce.repositories.base import BaseRepository
from app.utils import Validation


class PermissionSetRepository(BaseRepository):
    """
    Repository responsible for retrieving Salesforce Permission Sets.
    """

    def find_by_id( self, permission_set_id: str ) -> PermissionSet | None:
        Validation.validate_required( "permission_set_id", permission_set_id )

        response = self.query_executor.execute(
            query = PermissionSetQueries.by_id( permission_set_id )
        )

        record = self._get_first_record( response )

        if record is None:
            return None

        return PermissionSetMapper.from_record( record )

    def find_by_ids( self, permission_set_ids: set[ str ]) -> list[ PermissionSet ]:
        if not permission_set_ids:
            return []

        response = self.query_executor.execute(
            query = PermissionSetQueries.by_ids( permission_set_ids )
        )

        records = response.get( "records", [] )

        return [
            PermissionSetMapper.from_record( record )
            for record in records
        ]