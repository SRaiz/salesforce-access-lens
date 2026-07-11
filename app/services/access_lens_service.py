from app.utils import Validation
from app.application import UserAccessAnalysis
from app.salesforce.repositories import (
    UserRepository, 
    ProfileRepository, 
    PermissionSetAssignmentRepository, 
    PermissionSetRepository, 
    ObjectPermissionRepository, 
    FieldPermissionRepository
)
from app.salesforce.domain import (
    SalesforceUser, 
    Profile, 
    PermissionSet, 
    ObjectPermission, 
    FieldPermission
)

class AccessLensService:
    """
    Coordinates Salesforce repositories to produce a complete
    access analysis for a user.
    """
    
    def __init__(
        self, 
        user_repository                             : UserRepository, 
        profile_repository                          : ProfileRepository, 
        permission_set_assignment_repository        : PermissionSetAssignmentRepository, 
        permission_set_repository                   : PermissionSetRepository, 
        object_permission_repository                : ObjectPermissionRepository, 
        field_permission_repository                 : FieldPermissionRepository
    ) -> None:
        self._user_repository                               = user_repository
        self._profile_repository                            = profile_repository
        self._permission_set_assignment_repository          = permission_set_assignment_repository
        self._permission_set_repository                     = permission_set_repository
        self._object_permission_repository                  = object_permission_repository
        self._field_permission_repository                   = field_permission_repository
        
    @property
    def user_repository( self ) -> UserRepository:
        return self._user_repository
        
    @property
    def profile_repository( self ) -> ProfileRepository:
        return self._profile_repository
        
    @property
    def permission_set_assignment_repository( self ) -> PermissionSetAssignmentRepository:
        return self._permission_set_assignment_repository
        
    @property
    def permission_set_repository( self ) -> PermissionSetRepository:
        return self._permission_set_repository
        
    @property
    def object_permission_repository( self ) -> ObjectPermissionRepository:
        return self._object_permission_repository
        
    @property
    def field_permission_repository( self ) -> FieldPermissionRepository:
        return self._field_permission_repository
    
    def analyze_user( self, username: str ) -> UserAccessAnalysis:
        Validation.validate_required( "username", username )
        
        user = self._find_user_by_username( username )
        profile = self._find_profile( user.profile_id )
        
        permission_sets = self._find_permission_sets( user.user_id )
        
        profile_permission_sets = list(
            filter(
                lambda permission_set: permission_set.is_profile_owned(), 
                permission_sets
            )
        )
        
        assigned_permission_sets = list(
            filter(
                lambda permission_set: permission_set.is_standalone_permission_set(), 
                permission_sets
            )
        )
        
        permission_set_ids = {
            permission_set.permission_set_id
            for permission_set in permission_sets
        }
        
        object_permissions = self._find_object_permissions( permission_set_ids )
        field_permissions = self._find_field_permissions( permission_set_ids )
        
        return UserAccessAnalysis(
            user                        = user, 
            profile                     = profile, 
            profile_permission_sets     = profile_permission_sets, 
            assigned_permission_sets    = assigned_permission_sets, 
            object_permissions          = object_permissions, 
            field_permissions           = field_permissions
        )
    
    def _find_user_by_id( self, user_id: str ) -> SalesforceUser:
        user = self.user_repository.find_by_id( user_id )
        
        if user is None:
            raise ValueError(
                f"Salesforce user was not found for Id: { user_id }"
            )

        return user

    def _find_user_by_username( self, username: str ) -> SalesforceUser:
        user = self.user_repository.find_by_username( username )

        if user is None:
            raise ValueError(
                f"Salesforce user was not found for username: { username }"
            )

        return user

    def _find_user_by_email( self, email: str ) -> SalesforceUser:
        user = self.user_repository.find_by_email( email )

        if user is None:
            raise ValueError(
                f"Salesforce user was not found for email: { email }"
            )

        return user

    def _find_profile( self, profile_id: str ) -> Profile:
        profile = self.profile_repository.find_by_id( profile_id )

        if profile is None:
            raise ValueError(
                f"Salesforce Profile was not found for Id: { profile_id }"
            )

        return profile

    def _find_permission_sets( self, user_id: str ) -> list[ PermissionSet ]:
        # Retrieve all Permission Set Assignments for the user.
        assignments = (
            self.permission_set_assignment_repository.find_by_user_id(
                user_id
            )
        )

        # Extract Permission Set Ids from the permission set assignments.
        permission_set_ids = {
            assignment.permission_set_id
            for assignment in assignments
        }

        return self.permission_set_repository.find_by_ids(
            permission_set_ids
        )

    def _find_object_permissions( self, parent_ids: set[str] ) -> list[ ObjectPermission ]:
        
        return self.object_permission_repository.find_by_parent_ids(
            parent_ids
        )

    def _find_field_permissions( self, parent_ids: set[str] ) -> list[FieldPermission]:

        return self.field_permission_repository.find_by_parent_ids(
            parent_ids
        )