from app.utils import Validation

class Profile():
    """
    Represents a Salesforce Profile within the Salesforce Access Lens domain.
    """

    def __init__(
        self,
        profile_id  : str,
        name        : str
    ) -> None:
        Validation.validate_required( "profile_id", profile_id )
        Validation.validate_required( "name", name )

        self._profile_id    = profile_id
        self._name          = name

        self._object_permissions    = list()
        self._field_permissions     = list()

    @property
    def profile_id( self ) -> str:
        return self._profile_id

    @property
    def name( self ) -> str:
        return self._name

    @property
    def object_permissions( self ) -> list:
        return list( self._object_permissions )

    @property
    def field_permissions( self ) -> list:
        return list( self._field_permissions )

    def add_object_permission(
        self,
        object_permission: object,
    ) -> None:
        self._object_permissions.append( object_permission )

    def add_field_permission(
        self,
        field_permission: object,
    ) -> None:
        self._field_permissions.append( field_permission )

    def __repr__(self) -> str:
        return (
            "\n"
            f"Profile ID        : { self.profile_id }\n"
            f"Profile Name      : { self.name }\n"
        )

    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, Profile ):
            return NotImplemented

        return self._profile_id == other._profile_id

    def __hash__(self) -> int:
        return hash( self._profile_id )