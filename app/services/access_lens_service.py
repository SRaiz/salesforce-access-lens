from app.utils import Validation
from app.application import UserAccessAnalysis, PermissionSetAnalysis
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
        
        permission_set_ids = {
            permission_set.permission_set_id
            for permission_set in permission_sets
        }
        
        object_permissions = self._find_object_permissions( permission_set_ids )
        field_permissions = self._find_field_permissions( permission_set_ids )
        
        permission_set_analyses = self._build_permission_set_analyses(
            permission_sets, 
            object_permissions, 
            field_permissions
        )
        
        profile_permission_set_analyses = list(
            filter(
                lambda analysis: analysis.permission_set.is_profile_owned(), 
                permission_set_analyses
            )
        )
        
        assigned_permission_set_analyses = list(
            filter(
                lambda analysis: analysis.permission_set.is_standalone_permission_set(), 
                permission_set_analyses
            )
        )
        
        return UserAccessAnalysis(
            user                                = user, 
            profile                             = profile, 
            profile_permission_set_analyses     = profile_permission_set_analyses, 
            assigned_permission_set_analyses    = assigned_permission_set_analyses
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
        
    def _build_permission_set_analyses(
        self, 
        permission_sets         : list[ PermissionSet ], 
        object_permissions      : list[ ObjectPermission ], 
        field_permissions       : list[ FieldPermission ]
    ) -> list[ PermissionSetAnalysis ]:
        # We need to create a map of Permission set Id to its object and field permissions list
        object_permissions_by_parent = self._group_object_permissions_by_parent( object_permissions )
        field_permissions_by_parent = self._group_field_permissions_by_parent( field_permissions )
        
        return list(
            map(
                lambda permission_set: self._build_permission_set_analysis(
                    permission_set, 
                    object_permissions_by_parent.get( permission_set.permission_set_id, [] ), 
                    field_permissions_by_parent.get( permission_set.permission_set_id, [] )
                ),
                permission_sets
            )
        )
        
    def _group_object_permissions_by_parent(
        self, 
        object_permissions: list[ ObjectPermission ] 
    ) -> dict[ str, list[ ObjectPermission ]]:
        object_permissions_by_parent: dict[ str, list[ ObjectPermission ]] = dict()
        
        for permission in object_permissions:
            object_permissions_by_parent.setdefault(
                permission.parent_id, []
            ).append( permission )
            
        return object_permissions_by_parent
        
    def _group_field_permissions_by_parent(
        self, 
        field_permissions: list[ FieldPermission ] 
    ) -> dict[ str, list[ FieldPermission ]]:
        field_permissions_by_parent: dict[ str, list[ FieldPermission ]] = dict()
        
        for permission in field_permissions:
            field_permissions_by_parent.setdefault(
                permission.parent_id, []
            ).append( permission )
            
        return field_permissions_by_parent
            
    def _build_permission_set_analysis(
        self, 
        permission_set      : PermissionSet, 
        object_permissions  : list[ ObjectPermission ], 
        field_permissions   : list[ FieldPermission ]
    ) -> PermissionSetAnalysis:
        return PermissionSetAnalysis(
            permission_set          = permission_set,
            object_permissions      = object_permissions, 
            field_permissions       = field_permissions
        )