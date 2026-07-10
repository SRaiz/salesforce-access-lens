from app.utils import Validation

class FieldPermission:
    """
    Represents field-level access granted by a Profile-owned
    or standalone Salesforce Permission Set.
    """
    
    def __init__(
        self, 
        field_permission_id         : str, 
        field_api_name              : str, 
        parent_id                   : str, 
        sobject_type                : str, 
        can_read                    : bool, 
        can_edit                    : bool
    ) -> None:
        Validation.validate_required( "field_permission_id", field_permission_id )
        Validation.validate_required( "field_api_name", field_api_name )
        Validation.validate_required( "parent_id", parent_id )
        Validation.validate_required( "sobject_type", sobject_type )
        
        self._field_permission_id           = field_permission_id
        self._field_api_name                = field_api_name
        self._parent_id                     = parent_id
        self._sobject_type                  = sobject_type
        self._can_read                      = can_read
        self._can_edit                      = can_edit
        
    @property
    def field_permission_id( self ) -> str:
        return self._field_permission_id
        
    @property
    def field_api_name( self ) -> str:
        return self._field_api_name
        
    @property
    def parent_id( self ) -> str:
        return self._parent_id
        
    @property
    def sobject_type( self ) -> str:
        return self._sobject_type
        
    @property
    def can_read( self ) -> bool:
        return self._can_read
       
    @property
    def can_edit( self ) -> bool:
        return self._can_edit
    
    @property
    def object_name( self ) -> str:
        return self.sobject_type

    @property
    def field_name( self ) -> str:
        if "." in self.field_api_name:
            return self.field_api_name.split( ".", 1 )[1]
        
        return self.field_api_name
    
    def can_access_field( self ) -> bool:
        return self.can_read
    
    def has_read_only_access( self ) -> bool:
        return (
            self.can_read
            and not self.can_edit
        )
        
    def has_edit_access( self ) -> bool:
        return self.can_edit
    
    def has_no_field_access( self ) -> bool:
        return not any(
            (
                self.can_read, 
                self.can_edit
            )
        )
        
    def __repr__( self ) -> str:
        return (
            "\n"
            f"Field Permission Id           : { self.field_permission_id }\n"
            f"Object Name                   : { self.object_name }\n"
            f"Field Name                    : { self.field_name }\n"
            f"Parent Id                     : { self.parent_id }\n"
            f"SObject Type                  : { self.sobject_type }\n"
            f"Can Read                      : { self.can_read }\n"
            f"Can Edit                      : { self.can_edit }\n"
        )

    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, FieldPermission ):
            return NotImplemented

        return self._field_permission_id == other._field_permission_id

    def __hash__( self ) -> int:
        return hash( self._field_permission_id )