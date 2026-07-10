from app.utils import Validation

class PermissionSet:

    def __init__(
        self,
        permission_set_id   : str,
        label               : str,
        name                : str,
        profile_id          : str | None,
        user_license_id     : str | None,
        namespace_prefix    : str | None, 
        is_owned_by_profile : bool
    ) -> None:
        Validation.validate_required( "permission_set_id", permission_set_id )
        Validation.validate_required( "label", label )
        Validation.validate_required( "name", name )

        self._permission_set_id     = permission_set_id
        self._label                 = label
        self._name                  = name
        self._profile_id            = profile_id
        self._user_license_id       = user_license_id
        self._namespace_prefix      = namespace_prefix
        self._is_owned_by_profile   = is_owned_by_profile

    @property
    def permission_set_id( self ) -> str:
        return self._permission_set_id

    @property
    def label( self ) -> str:
        return self._label

    @property
    def name( self ) -> str:
        return self._name

    @property
    def profile_id( self ) -> str | None:
        return self._profile_id

    @property
    def user_license_id( self ) -> str | None:
        return self._user_license_id

    @property
    def namespace_prefix( self ) -> str | None:
        return self._namespace_prefix

    def is_profile_owned( self ) -> bool:
        return self._is_owned_by_profile

    def is_managed_package_permission_set( self ) -> bool:
        return self._namespace_prefix is not None

    def is_standalone_permission_set( self ) -> bool:
        return not self._is_owned_by_profile

    def __repr__( self ) -> str:
        return (
            "\n"
            f"Permission Set Id       : { self.permission_set_id }\n"
            f"Permission Set Label    : { self.label }\n"
            f"Permission Set Name     : { self.name }\n"
            f"Profile Id              : { self.profile_id }\n"
            f"User License Id         : { self.user_license_id }\n"
            f"Namespace Prefix        : { self.namespace_prefix }\n"
            f"Is Profile Owned        : { self.is_profile_owned() }\n"
            f"Is Managed Package      : { self.is_managed_package_permission_set() }\n"
            f"Is Standalone           : { self.is_standalone_permission_set() }\n"
        )

    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, PermissionSet ):
            return NotImplemented

        return self._permission_set_id == other._permission_set_id

    def __hash__( self ) -> int:
        return hash( self._permission_set_id )