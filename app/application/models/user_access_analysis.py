from app.salesforce.domain import (
    SalesforceUser,
    Profile, 
    ObjectPermission,  
    FieldPermission, 
    PermissionSet
)
class UserAccessAnalysis:
    """
    Represents the complete Salesforce access analysis for one user.
    """
    
    def __init__(
        self, 
        user                        : SalesforceUser, 
        profile                     : Profile, 
        profile_permission_sets     : list[ PermissionSet ], 
        assigned_permission_sets    : list[ PermissionSet ], 
        object_permissions          : list[ ObjectPermission ], 
        field_permissions           : list[ FieldPermission ]
    ) -> None:
        self._user                        = user
        self._profile                     = profile
        self._profile_permission_sets     = profile_permission_sets
        self._assigned_permission_sets    = assigned_permission_sets
        self._object_permissions          = object_permissions
        self._field_permissions           = field_permissions
    
    @property 
    def user( self ) -> SalesforceUser:
        return self._user
    
    @property 
    def profile( self ) -> Profile:
        return self._profile
    
    @property 
    def profile_permission_sets( self ) -> list[ PermissionSet ]:
        return self._profile_permission_sets
    
    @property 
    def assigned_permission_sets( self ) -> list[ PermissionSet ]:
        return self._assigned_permission_sets
    
    @property 
    def object_permissions( self ) -> list[ ObjectPermission ]:
        return self._object_permissions
    
    @property 
    def field_permissions( self ) -> list[ FieldPermission ]:
        return self._field_permissions
    
    @property
    def all_permission_sets( self ) -> list[ PermissionSet ]:
        return [
            * self.profile_permission_sets, 
            * self.assigned_permission_sets
        ]
        
    def __repr__( self ):
        return (
            "\n"
            f"User                         : { self.user.username }\n"
            f"Profile                      : { self.profile.name }\n"
            f"Profile Permission Sets      : { len( self.profile_permission_sets )}\n"
            f"Assigned Permission Sets     : { len( self.assigned_permission_sets )}\n"
            f"Object Permissions           : { len( self.object_permissions )}\n"
            f"Field Permissions            : { len( self.field_permissions )}\n"
        )