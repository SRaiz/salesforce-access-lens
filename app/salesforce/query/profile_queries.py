class ProfileQueries:
    
    """
    Builds SOQL queries related to Salesforce User records.
    """
    PROFILE_FIELDS = [
        "Id", 
        "Name", 
        "UserLicenseId"
    ]
    
    @classmethod
    def by_id( cls, profile_id: str ):
        escaped_profile_id = cls._escape_soql_value( profile_id )
        
        return cls._select_profile_query(
            where_clause = f"Id = '{ escaped_profile_id }'"
        )
    
    @classmethod
    def _select_profile_query( cls, where_clause: str ) -> str:
        fields = ", ".join(cls.PROFILE_FIELDS)
        
        return f"SELECT { fields } FROM Profile WHERE { where_clause } LIMIT 1"

    @staticmethod
    def _escape_soql_value( value: str ) -> str:
        return value.replace("\\", "\\\\").replace("'", "\\'")