from app.salesforce.domain import FieldPermission


class FieldPermissionMapper:
    """
    Maps Salesforce FieldPermissions records into
    FieldPermission domain entities.
    """

    @staticmethod
    def from_record( record: dict ) -> FieldPermission:
        """
        Converts a Salesforce FieldPermissions record
        into a FieldPermission domain entity.
        """

        return FieldPermission(
            field_permission_id     = record[ "Id" ],
            field_api_name          = record[ "Field" ],
            parent_id               = record[ "ParentId" ],
            sobject_type            = record[ "SobjectType" ],
            can_read                = record[ "PermissionsRead" ],
            can_edit                = record[ "PermissionsEdit" ]
        )