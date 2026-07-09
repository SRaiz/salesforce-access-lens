from app.salesforce.domain import Profile

class ProfileMapper:
    """
    Maps Salesforce Profile records into Profile domain entities.
    """

    @staticmethod
    def from_record( record: dict ) -> Profile:
        """
        Converts a Salesforce Profile record into a Profile domain entity.
        """

        return Profile(
            profile_id  = record[ "Id" ], 
            name        = record[ "Name" ], 
        )