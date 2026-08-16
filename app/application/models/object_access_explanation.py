from app.utils import Validation
from .object_permission_source import ObjectPermissionSource


class ObjectAccessExplanation:
    """
    Represents the combined effective object access and every
    Permission Set source contributing to that access.
    """
    
    def __init__(
        self, 
        object_name     : str, 
        sources         : list[ ObjectPermissionSource ]
    ) -> None:
        Validation.validate_required( "object_name", object_name )
        
        self._validate_sources( object_name, sources )
        
        self._object_name       = object_name
        self._sources           = sources
        
    @property
    def object_name( self ) -> str:
        return self._object_name
        
    @property
    def sources( self ) -> list[ ObjectPermissionSource ]:
        return self._sources
        
    @property
    def source_count( self ) -> int:
        return len( self.sources )
        
    def has_access( self ) -> bool:
        return any(
            (
                self.can_read(),
                self.can_create(),
                self.can_edit(),
                self.can_delete(),
                self.can_view_all_records(),
                self.can_modify_all_records()
            )
        )
        
    def can_read( self ) -> bool:
        return any(
            map(
                lambda source: source.can_read(), 
                self.sources
            )
        )
        
    def can_create( self ) -> bool:
        return any(
            map(
                lambda source: source.can_create(), 
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
        
    def can_delete( self ) -> bool:
        return any(
            map(
                lambda source: source.can_delete(), 
                self.sources
            )
        )
        
    def can_view_all_records( self ) -> bool:
        return any(
            map(
                lambda source: source.can_view_all_records(), 
                self.sources
            )
        )
        
    def can_modify_all_records( self ) -> bool:
        return any(
            map(
                lambda source: source.can_modify_all_records(), 
                self.sources
            )
        )
        
    def can_view_all_fields( self ) -> bool:
        return any(
            map(
                lambda source: source.can_view_all_fields(), 
                self.sources
            )
        )
        
    @staticmethod
    def _validate_sources(
        object_name     : str, 
        sources         : list[ ObjectPermissionSource ]
    ) -> None:
        mismatched_sources = list(
            filter(
                lambda source: source.object_name != object_name, 
                sources
            )
        )
        
        if mismatched_sources:
            mismatched_object_names = {
                source.object_name
                for source in mismatched_sources
            }
            
            raise ValueError(
                "ObjectAccessExplanation source mismatch: "
                f"expected all sources to belong to "
                f"'{ object_name }', "
                f"but received sources for "
                f"{ sorted( mismatched_object_names ) }."
            )
        
    def __repr__( self ) -> str:
        return (
            "\n"
            f"Object                       : { self.object_name }\n"
            f"Has Access                   : { self.has_access() }\n"
            f"Can Read                     : { self.can_read() }\n"
            f"Can Create                   : { self.can_create() }\n"
            f"Can Edit                     : { self.can_edit() }\n"
            f"Can Delete                   : { self.can_delete() }\n"
            f"Can View All Records         : { self.can_view_all_records() }\n"
            f"Can Modify All Records       : { self.can_modify_all_records() }\n"
            f"Can View All Fields          : { self.can_view_all_fields() }\n"
            f"Permission Source Count      : { self.source_count }\n"
        )