from app.salesforce.domain import (
    Profile,
    PermissionSet,
    FieldPermission
)


class FieldPermissionSource:
    """
    Associates a FieldPermission with the PermissionSet
    responsible for granting it.
    """

    def __init__(
        self,
        permission_set      : PermissionSet,
        field_permission    : FieldPermission,
        profile             : Profile | None
    ) -> None:
        # Validate that the FieldPermission belongs to the PermissionSet.
        if permission_set.permission_set_id != field_permission.parent_id:
            raise ValueError(
                "FieldPermission source mismatch: "
                f"Expected parent_id "
                f"'{ permission_set.permission_set_id }', "
                f"but received "
                f"'{ field_permission.parent_id }'."
            )

        # Validate the Profile relationship for a profile-owned source.
        if permission_set.is_profile_owned():
            if profile is None:
                raise ValueError(
                    "A Profile must be provided when the Permission Set "
                    "is profile-owned."
                )

            if permission_set.profile_id != profile.profile_id:
                raise ValueError(
                    "Profile source mismatch: "
                    f"Permission Set references Profile Id "
                    f"'{ permission_set.profile_id }', "
                    f"but received Profile Id "
                    f"'{ profile.profile_id }'."
                )

        # A standalone Permission Set must not have a Profile.
        elif profile is not None:
            raise ValueError(
                "A Profile cannot be provided for a standalone "
                "Permission Set source."
            )

        self._permission_set        = permission_set
        self._field_permission     = field_permission
        self._profile              = profile

    @property
    def permission_set( self ) -> PermissionSet:
        return self._permission_set

    @property
    def field_permission( self ) -> FieldPermission:
        return self._field_permission

    @property
    def profile( self ) -> Profile | None:
        return self._profile

    @property
    def object_name( self ) -> str:
        return self.field_permission.object_name

    @property
    def field_name( self ) -> str:
        return self.field_permission.field_name

    @property
    def field_api_name( self ) -> str:
        return self.field_permission.field_api_name

    @property
    def source_name( self ) -> str:
        return (
            self.profile.name
            if self.profile is not None
            else self.permission_set.label
        )

    # Source Classification Capabilities
    def is_profile_source( self ) -> bool:
        return self.permission_set.is_profile_owned()

    def is_assigned_permission_set_source( self ) -> bool:
        return self.permission_set.is_standalone_permission_set()

    def is_managed_package_source( self ) -> bool:
        return self.permission_set.is_managed_package_permission_set()

    # Permission Capabilities
    def can_read( self ) -> bool:
        return self.field_permission.can_read

    def can_edit( self ) -> bool:
        return self.field_permission.can_edit

    def __repr__( self ) -> str:
        return (
            "\n"
            f"Object                       : { self.object_name }\n"
            f"Field                        : { self.field_name }\n"
            f"Field API Name               : { self.field_api_name }\n"
            f"Source Name                  : { self.source_name }\n"
            f"Permission Set Id            : { self.permission_set.permission_set_id }\n"
            f"Profile Source               : { self.is_profile_source() }\n"
            f"Assigned Permission Set      : { self.is_assigned_permission_set_source() }\n"
            f"Managed Package Source       : { self.is_managed_package_source() }\n"
            f"Can Read                     : { self.can_read() }\n"
            f"Can Edit                     : { self.can_edit() }\n"
        )