from app.utils import Validation
from app.salesforce.domain import Profile
from app.salesforce.mappers import ProfileMapper
from app.salesforce.query import ProfileQueries
from app.salesforce.repositories.base import BaseRepository


class ProfileRepository( BaseRepository[ Profile ] ):
    """
    Repository responsible for retrieving Salesforce profiles.
    """

    def find_by_id( self, profile_id: str ) -> Profile | None:
        """
        Finds a Salesforce profile by Profile Id.
        """

        Validation.validate_required( "profile_id", profile_id )

        response = self.query_executor.execute(
            query = ProfileQueries.by_id( profile_id )
        )

        record = self._get_first_record( response )
        if record is None:
            return None

        return ProfileMapper.from_record( record )