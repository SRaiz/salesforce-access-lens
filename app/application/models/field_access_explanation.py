from app.utils import Validation
from .field_permission_source import FieldPermissionSource


class FieldAccessExplanation:
    """
    Represents the combined effective field access and every
    Permission Set source contributing to that access.
    """

    def __init__(
        self,
        object_name     : str,
        field_name      : str,
        sources         : list[ FieldPermissionSource ]
    ) -> None:
        Validation.validate_required( "object_name", object_name )
        Validation.validate_required( "field_name", field_name )

        self._validate_sources(
            object_name,
            field_name,
            sources
        )

        self._object_name      = object_name
        self._field_name       = field_name
        self._sources          = sources

    @property
    def object_name( self ) -> str:
        return self._object_name

    @property
    def field_name( self ) -> str:
        return self._field_name

    @property
    def field_api_name( self ) -> str:
        return f"{ self.object_name }.{ self.field_name }"

    @property
    def sources( self ) -> list[ FieldPermissionSource ]:
        return self._sources

    @property
    def source_count( self ) -> int:
        return len( self.sources )

    def has_access( self ) -> bool:
        return any(
            (
                self.can_read(),
                self.can_edit()
            )
        )

    def can_read( self ) -> bool:
        return any(
            map(
                lambda source: source.can_read(),
                self.sources
            )
        )

    def can_edit( self ) -> bool:
        return any(
            map(
                lambda source: source.can_edit(),
                self.sources
            )
        )

    @staticmethod
    def _validate_sources(
        object_name     : str,
        field_name      : str,
        sources         : list[ FieldPermissionSource ]
    ) -> None:
        mismatched_sources = list(
            filter(
                lambda source: (
                    source.object_name != object_name
                    or source.field_name != field_name
                ),
                sources
            )
        )

        if mismatched_sources:
            expected_field_api_name = (
                f"{ object_name }.{ field_name }"
            )

            mismatched_field_api_names = {
                source.field_api_name
                for source in mismatched_sources
            }

            raise ValueError(
                "FieldAccessExplanation source mismatch: "
                f"expected all sources to belong to "
                f"'{ expected_field_api_name }', "
                f"but received sources for "
                f"{ sorted( mismatched_field_api_names ) }."
            )

    def __repr__( self ) -> str:
        return (
            "\n"
            f"Object                       : { self.object_name }\n"
            f"Field                        : { self.field_name }\n"
            f"Field API Name               : { self.field_api_name }\n"
            f"Has Access                   : { self.has_access() }\n"
            f"Can Read                     : { self.can_read() }\n"
            f"Can Edit                     : { self.can_edit() }\n"
            f"Permission Source Count      : { self.source_count }\n"
        )