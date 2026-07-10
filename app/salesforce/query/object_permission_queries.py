class ObjectPermissionQueries:
    """
    Builds SOQL queries related to ObjectPermission records.
    """
    
    OBJECT_PERMISSION_FIELDS = [
        "Id", 
        "ParentId", 
        "SobjectType", 
        "PermissionsRead", 
        "PermissionsCreate", 
        "PermissionsEdit", 
        "PermissionsDelete", 
        "PermissionsViewAllRecords", 
        "PermissionsModifyAllRecords",
        "PermissionsViewAllFields"
    ]
    
    @classmethod
    def by_parent_id( cls, parent_id: str ) -> str:
        escaped_parent_id = cls._escape_soql_value( parent_id )
        
        return cls._select_object_permission_query(
            where_clause = f"ParentId = '{ escaped_parent_id }'"
        )
    
    @classmethod
    def by_parent_ids( cls, parent_ids: set[ str ]) -> str:
        
        if not parent_ids:
            raise ValueError( "At least one parent Permission set Id must be provided." )
        
        escaped_parent_ids = ", ".join(
            f"'{ cls._escape_soql_value( parent_id ) }'"
            for parent_id in sorted( parent_ids )
        )
        
        return cls._select_object_permission_query(
            where_clause = f"ParentId IN ({ escaped_parent_ids })"
        )
        
    @classmethod
    def _select_object_permission_query( cls, where_clause: str ) -> str:
        fields = ", ".join( cls.OBJECT_PERMISSION_FIELDS )

        return (
            "SELECT "
            f"{ fields } "
            "FROM ObjectPermissions "
            f"WHERE { where_clause }"
        )
        
    @staticmethod
    def _escape_soql_value( value: str ) -> str:
        return value.replace( "\\", "\\\\" ).replace( "'", "\\'" )