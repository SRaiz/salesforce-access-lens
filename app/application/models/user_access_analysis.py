from .permission_set_analysis import PermissionSetAnalysis
from app.salesforce.domain import (
    SalesforceUser,
    Profile, 
    ObjectPermission,  
    FieldPermission 
)
class UserAccessAnalysis:
    """
    Represents the complete Salesforce access analysis for one user.
    """
    
    def __init__(
        self, 
        user                                    : SalesforceUser, 
        profile                                 : Profile, 
        profile_permission_set_analyses         : list[ PermissionSetAnalysis ],
        assigned_permission_set_analyses        : list[ PermissionSetAnalysis ]
    ) -> None:
        self._user                                  = user
        self._profile                               = profile
        self._profile_permission_set_analyses       = profile_permission_set_analyses
        self._assigned_permission_set_analyses      = assigned_permission_set_analyses
    
    @property 
    def user( self ) -> SalesforceUser:
        return self._user
    
    @property 
    def profile( self ) -> Profile:
        return self._profile
    
    @property
    def profile_permission_set_analyses( self ) -> list[PermissionSetAnalysis]:
        return self._profile_permission_set_analyses


    @property
    def assigned_permission_set_analyses( self ) -> list[PermissionSetAnalysis]:
        return self._assigned_permission_set_analyses


    @property
    def all_permission_set_analyses( self ) -> list[PermissionSetAnalysis]:
        return [
            * self.profile_permission_set_analyses,
            * self.assigned_permission_set_analyses
        ]
    
    def get_object_permission( self, object_name: str ) -> ObjectPermission | None:
        
        for permission_set_analysis in self.all_permission_set_analyses:
            permission = permission_set_analysis.get_object_permission(
                object_name
            )
            
            if permission is not None:
                return permission
        
        return None
        
    def can_read_object( self, object_name: str ) -> bool:
        permission = self.get_object_permission( object_name )

        return (
            permission.can_read
            if permission is not None
            else False
        )


    def can_create_object( self, object_name: str ) -> bool:
        permission = self.get_object_permission( object_name )

        return (
            permission.can_create
            if permission is not None
            else False
        )


    def can_edit_object( self, object_name: str ) -> bool:
        permission = self.get_object_permission( object_name )

        return (
            permission.can_edit
            if permission is not None
            else False
        )


    def can_delete_object( self, object_name: str ) -> bool:
        permission = self.get_object_permission( object_name )

        return (
            permission.can_delete
            if permission is not None
            else False
        )
        
    def get_field_permission(
        self, 
        object_name : str, 
        field_name  : str
    ) -> FieldPermission | None:
        
        for permission_set_analysis in self.all_permission_set_analyses:
            permission = permission_set_analysis.get_field_permission(
                object_name,
                field_name
            )
            
            if permission is not None:
                return permission
        
        return None
        
    def can_read_field(
        self, 
        object_name : str, 
        field_name  : str
    ) -> bool:
        
        permission = self.get_field_permission(
            object_name, 
            field_name
        )
        
        return (
            permission.can_read 
            if permission is not None 
            else False
        )
        
    def can_edit_field(
        self, 
        object_name : str, 
        field_name  : str
    ) -> bool:
        
        permission = self.get_field_permission(
            object_name, 
            field_name
        )
        
        return (
            permission.can_edit 
            if permission is not None 
            else False
        )
        
    def __repr__( self ):
        return (
            "\n"
            f"User                                  : { self.user.username }\n"
            f"Profile                               : { self.profile.name }\n"
            f"Profile Permission Sets Analyses      : { len( self.profile_permission_set_analyses )}\n"
            f"Assigned Permission Sets Analyses     : { len( self.assigned_permission_set_analyses )}\n"
        )