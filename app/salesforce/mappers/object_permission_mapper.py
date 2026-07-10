from app.salesforce.domain import ObjectPermission


class ObjectPermissionMapper:
    """
    Maps Salesforce ObjectPermissions records into ObjectPermission domain entities.
    """

    @staticmethod
    def from_record( record: dict ) -> ObjectPermission:
        """
        Converts a Salesforce ObjectPermissions record into a domain entity.
        """

        return ObjectPermission(
            object_permission_id        = record[ "Id" ],
            parent_id                   = record[ "ParentId" ],
            sobject_type                = record[ "SobjectType" ],
            can_read                    = record[ "PermissionsRead" ],
            can_create                  = record[ "PermissionsCreate" ],
            can_edit                    = record[ "PermissionsEdit" ],
            can_delete                  = record[ "PermissionsDelete" ],
            can_view_all_records        = record[ "PermissionsViewAllRecords" ],
            can_modify_all_records      = record[ "PermissionsModifyAllRecords" ],
            can_view_all_fields         = record[ "PermissionsViewAllFields" ]
        )