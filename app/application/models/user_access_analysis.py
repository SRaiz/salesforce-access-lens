from app.utils import Validation
from .permission_set_analysis import PermissionSetAnalysis
from .object_permission_source import ObjectPermissionSource
from .object_access_explanation import ObjectAccessExplanation
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
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_read()


    def can_create_object( self, object_name: str ) -> bool:
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_create()


    def can_edit_object( self, object_name: str ) -> bool:
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_edit()


    def can_delete_object( self, object_name: str ) -> bool:
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_delete()
    
    def can_view_all_records( self, object_name: str ) -> bool:
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_view_all_records()


    def can_modify_all_records( self, object_name: str ) -> bool:
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_modify_all_records()


    def can_view_all_fields( self, object_name: str ) -> bool:
        explanation = self.explain_object_access(
            object_name
        )
        
        return explanation.can_view_all_fields()
        
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
        
    def explain_object_access(
        self, 
        object_name: str
    ) -> ObjectAccessExplanation:
        
        """
        Explains the user's effective access to an object across
        every contributing Permission Set.
        """
        Validation.validate_required( "object_name", object_name )
        
        possible_sources = map(
            lambda permission_set_analysis: (
                self._build_object_permission_source(
                    permission_set_analysis, 
                    object_name
                )
            ), 
            self.all_permission_set_analyses
        )
        
        sources = list(
            filter(
                lambda source: source is not None, 
                possible_sources
            )
        )
        
        return ObjectAccessExplanation(
            object_name     = object_name, 
            sources         = sources
        )
    
    def _build_object_permission_source(
        self, 
        permission_set_analysis   : PermissionSetAnalysis, 
        object_name               : str
    ) -> ObjectPermissionSource | None:

        object_permission = (
            permission_set_analysis.get_object_permission( object_name )
        )
        
        profile = (
            self.profile 
            if permission_set_analysis.permission_set.is_profile_owned() 
            else None
        )
        
        if object_permission is None:
            return None
            
        return ObjectPermissionSource(
            permission_set      = permission_set_analysis.permission_set, 
            object_permission   = object_permission, 
            profile             = profile
        )
        
        
    def __repr__( self ):
        return (
            "\n"
            f"User                                  : { self.user.username }\n"
            f"Profile                               : { self.profile.name }\n"
            f"Profile Permission Sets Analyses      : { len( self.profile_permission_set_analyses )}\n"
            f"Assigned Permission Sets Analyses     : { len( self.assigned_permission_set_analyses )}\n"
        )