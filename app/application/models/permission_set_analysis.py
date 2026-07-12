from app.salesforce.domain import (
    PermissionSet, 
    ObjectPermission, 
    FieldPermission
)

class PermissionSetAnalysis:
    
    def __init__(
        self, 
        permission_set      : PermissionSet, 
        object_permissions  : list[ ObjectPermission ], 
        field_permissions   : list[ FieldPermission ]
    ):
        self._permission_set        = permission_set
        self._object_permissions    = object_permissions
        self._field_permissions     = field_permissions
        
    @property
    def permission_set( self ) -> PermissionSet:
        return self._permission_set
        
    @property
    def object_permissions( self ) -> list[ ObjectPermission ]:
        return self._object_permissions
        
    @property
    def field_permissions( self ) -> list[ FieldPermission ]:
        return self._field_permissions
    
    def get_object_permission(
        self,
        object_name: str,
    ) -> ObjectPermission | None:
        return next(
            filter(
                lambda permission: (
                    permission.sobject_type == object_name
                ),
                self.object_permissions,
            ),
            None,
        )


    def get_field_permission(
        self,
        object_name: str,
        field_name: str,
    ) -> FieldPermission | None:
        return next(
            filter(
                lambda permission: (
                    permission.object_name == object_name
                    and permission.field_name == field_name
                ),
                self.field_permissions,
            ),
            None,
        )
    
    def __repr__(self) -> str:
        return (
            "\n"
            f"Permission Set               : { self.permission_set.label }\n"
            f"Profile Owned                : { self.permission_set.is_profile_owned() }\n"
            f"Object Permissions           : { len( self.object_permissions )}\n"
            f"Field Permissions            : { len( self.field_permissions )}\n"
        )