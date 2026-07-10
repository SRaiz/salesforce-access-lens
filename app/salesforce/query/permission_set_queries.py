class PermissionSetQueries:
    """
    Builds SOQL queries related to Permission Set records.
    """
    PERMISSION_SET_FIELDS = [
        "Id", 
        "Name", 
        "Label", 
        "ProfileId", 
        "LicenseId", 
        "NamespacePrefix", 
        "IsOwnedByProfile"
    ]
    
    @classmethod
    def by_id( cls, permission_set_id: str ) -> str:
        escaped_permission_set_id = cls._escape_soql_value( permission_set_id )
        
        return cls._select_permission_set_query(
            where_clause = f"Id = '{ escaped_permission_set_id }'"
        )
    
    @classmethod
    def by_ids( cls, permission_set_ids: set[str] ) -> str:
        
        if not permission_set_ids:
            raise ValueError( "At least one Permission Set Id must be provided." )
        
        escaped_permission_set_ids = ", ".join(
            f"'{ cls._escape_soql_value( permission_set_id ) }'"
            for permission_set_id in sorted( permission_set_ids )
        )
        
        return cls._select_permission_set_query(
            where_clause = f"Id IN ({ escaped_permission_set_ids })"
        )
        
    @classmethod
    def _select_permission_set_query( cls, where_clause: str ) -> str:
        fields = ", ".join( cls.PERMISSION_SET_FIELDS )

        return (
            "SELECT "
            f"{ fields } "
            "FROM PermissionSet "
            f"WHERE { where_clause }"
        )
        
    @staticmethod
    def _escape_soql_value( value: str ) -> str:
        return value.replace( "\\", "\\\\" ).replace( "'", "\\'" )