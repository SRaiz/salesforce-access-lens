from app.salesforce.domain import (
    Profile, 
    PermissionSet, 
    ObjectPermission
)

class ObjectPermissionSource:
    """
    Associates an ObjectPermission with the PermissionSet
    responsible for granting it.
    """
    
    def __init__(
        self, 
        permission_set      : PermissionSet, 
        object_permission   : ObjectPermission, 
        profile             : Profile | None
    ) -> None:
        
        # Validate permission_set and object_permission relate to each other
        if permission_set.permission_set_id != object_permission.parent_id:
            raise ValueError(
                "ObjectPermission source mismatch: "
                f"Expected parent_id "
                f"'{ permission_set.permission_set_id }', "
                f"but received "
                f"'{ object_permission.parent_id }'."
            )
            
        # A profile-owned Permission Set must include its Profile.
        if permission_set.is_profile_owned() and profile is None:
            raise ValueError(
                "A Profile must be provided when the Permission Set is profile-owned."
            )
            
        # The Profile must own the supplied Permission Set.
        if (
            profile is not None
            and permission_set.profile_id != profile.profile_id
        ):
            raise ValueError(
                "Profile source mismatch: "
                f"Permission Set references Profile Id "
                f"'{ permission_set.profile_id }', "
                f"but received Profile Id "
                f"'{ profile.profile_id }'."
            )
            
        # A standalone Permission Set must not have a Profile.
        if (
            permission_set.is_standalone_permission_set()
            and profile is not None
        ):
            raise ValueError(
                "A Profile cannot be provided for a standalone Permission Set source."
            )
            
        self._permission_set        = permission_set
        self._object_permission     = object_permission
        self._profile               = profile
    
    @property
    def permission_set( self ) -> PermissionSet:
        return self._permission_set
    
    @property
    def object_permission( self ) -> ObjectPermission:
        return self._object_permission
    
    @property
    def profile( self ) -> Profile | None:
        return self._profile
    
    @property
    def object_name( self ) -> str:
        return self.object_permission.sobject_type
    
    
    @property
    def source_name( self ) -> str:
        return (
            self.profile.name
            if self.profile is not None
            else self.permission_set.label
        )
    
    #   Source Classification Capabilities
    def is_profile_source( self ) -> bool:
        return self.permission_set.is_profile_owned()
    
    def is_assigned_permission_set_source( self ) -> bool:
        return self.permission_set.is_standalone_permission_set()
    
    def is_managed_package_source( self ) -> bool:
        return self.permission_set.is_managed_package_permission_set()
    
    #   Permission Capabilities
    def can_read( self ) -> bool:
        return self.object_permission.can_read
    
    def can_create( self ) -> bool:
        return self.object_permission.can_create
    
    def can_edit( self ) -> bool:
        return self.object_permission.can_edit
    
    def can_delete( self ) -> bool:
        return self.object_permission.can_delete
    
    def can_view_all_records( self ) -> bool:
        return self.object_permission.can_view_all_records
    
    def can_modify_all_records( self ) -> bool:
        return self.object_permission.can_modify_all_records
    
    def can_view_all_fields( self ) -> bool:
        return self.object_permission.can_view_all_fields
    
    def __repr__(self) -> str:
        return (
            "\n"
            f"Object                       : { self.object_name }\n"
            f"Source Name                  : { self.source_name }\n"
            f"Permission Set Id            : { self.permission_set.permission_set_id }\n"
            f"Profile Source               : { self.is_profile_source() }\n"
            f"Assigned Permission Set      : { self.is_assigned_permission_set_source() }\n"
            f"Managed Package Source       : { self.is_managed_package_source() }\n"
            f"Can Read                     : { self.can_read() }\n"
            f"Can Create                   : { self.can_create() }\n"
            f"Can Edit                     : { self.can_edit() }\n"
            f"Can Delete                   : { self.can_delete() }\n"
            f"Can View All Records         : { self.can_view_all_records() }\n"
            f"Can Modify All Records       : { self.can_modify_all_records() }\n"
            f"Can View All Fields          : { self.can_view_all_fields() }\n"
        )