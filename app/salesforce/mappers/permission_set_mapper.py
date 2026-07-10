from app.salesforce.domain import PermissionSet


class PermissionSetMapper:
    """
    Maps Salesforce PermissionSet records into PermissionSet domain entities.
    """

    @staticmethod
    def from_record( record: dict ) -> PermissionSet:
        """
        Converts a Salesforce PermissionSet record into a domain entity.
        """

        return PermissionSet(
            permission_set_id   = record[ "Id" ],
            label               = record[ "Label" ],
            name                = record[ "Name" ],
            profile_id          = record.get( "ProfileId" ),
            user_license_id     = record.get( "LicenseId" ),
            namespace_prefix    = record.get( "NamespacePrefix" ),
            is_owned_by_profile = record[ "IsOwnedByProfile" ]
        )