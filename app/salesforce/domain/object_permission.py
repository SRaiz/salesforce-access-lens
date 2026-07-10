from app.utils import Validation

class ObjectPermission:
    """
    Represents object-level access granted by a Profile-owned
    or standalone Salesforce Permission Set.
    """
    
    def __init__(
        self, 
        object_permission_id        : str, 
        parent_id                   : str, 
        sobject_type                : str, 
        can_read                    : bool, 
        can_create                  : bool, 
        can_edit                    : bool, 
        can_delete                  : bool, 
        can_view_all_records        : bool, 
        can_modify_all_records      : bool, 
        can_view_all_fields         : bool
    ) -> None:
        Validation.validate_required( "object_permission_id", object_permission_id )
        Validation.validate_required( "parent_id", parent_id )
        Validation.validate_required( "sobject_type", sobject_type )
        
        self._object_permission_id          = object_permission_id
        self._parent_id                     = parent_id
        self._sobject_type                  = sobject_type
        self._can_read                      = can_read
        self._can_create                    = can_create
        self._can_edit                      = can_edit
        self._can_delete                    = can_delete
        self._can_view_all_records          = can_view_all_records
        self._can_modify_all_records        = can_modify_all_records
        self._can_view_all_fields           = can_view_all_fields
        
    @property
    def object_permission_id( self ) -> str:
        return self._object_permission_id
        
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
    def can_create( self ) -> bool:
        return self._can_create
        
    @property
    def can_edit( self ) -> bool:
        return self._can_edit
        
    @property
    def can_delete( self ) -> bool:
        return self._can_delete
        
    @property
    def can_view_all_records( self ) -> bool:
        return self._can_view_all_records
        
    @property
    def can_modify_all_records( self ) -> bool:
        return self._can_modify_all_records
        
    @property
    def can_view_all_fields( self ) -> bool:
        return self._can_view_all_fields
    
    def can_access_object( self ) -> bool:
        return self._can_read

    def has_full_crud( self ) -> bool:
        return all(
            (
                self.can_read,
                self.can_create,
                self.can_edit,
                self.can_delete,
            )
        )

    def has_read_only_access( self ) -> bool:
        return (
            self.can_read
            and not self.can_create
            and not self.can_edit
            and not self.can_delete
        )

    def has_elevated_record_access( self ) -> bool:
        return (
            self.can_view_all_records
            or self.can_modify_all_records
        )
        
    def has_no_object_access( self ) -> bool:
        return not any(
            (
                self.can_read,
                self.can_create,
                self.can_edit,
                self.can_delete,
                self.can_view_all_records,
                self.can_modify_all_records,
            )
        )
    
    def __repr__( self ) -> str:
        return (
            "\n"
            f"Object Permission Id          : { self.object_permission_id }\n"
            f"Parent Id                     : { self.parent_id }\n"
            f"Sobject Type                  : { self.sobject_type }\n"
            f"Can Read                      : { self.can_read }\n"
            f"Can Create                    : { self.can_create }\n"
            f"Can Edit                      : { self.can_edit }\n"
            f"Can Delete                    : { self.can_delete }\n"
            f"Can View All Records          : { self.can_view_all_records }\n"
            f"Can Modify All Records        : { self.can_modify_all_records }\n"
            f"Can View All Fields           : { self.can_view_all_fields }\n"
        )

    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, ObjectPermission ):
            return NotImplemented

        return self._object_permission_id == other._object_permission_id

    def __hash__( self ) -> int:
        return hash( self._object_permission_id )