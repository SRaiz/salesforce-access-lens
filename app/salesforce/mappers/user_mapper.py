from app.salesforce.domain import SalesforceUser


class UserMapper:
    """
    Maps Salesforce User records into SalesforceUser domain entities.
    """

    @staticmethod
    def from_record( record: dict ) -> SalesforceUser:
        """
        Converts a Salesforce User record into a SalesforceUser domain entity.
        """

        return SalesforceUser(
            user_id     = record[ "Id" ],
            name        = record[ "Name" ],
            username    = record[ "Username" ],
            email       = record[ "Email" ],
            profile_id  = record[ "ProfileId" ],
            is_active   = record[ "IsActive" ],
            user_type   = record[ "UserType" ]
        )