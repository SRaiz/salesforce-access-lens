class UserQueries:
    """
    Builds SOQL queries related to Salesforce User records.
    """

    USER_FIELDS = [
        "Id",
        "Name",
        "Username",
        "Email",
        "ProfileId",
        "IsActive",
        "UserType",
    ]

    @classmethod
    def by_username( cls, username: str ) -> str:
        escaped_username = cls._escape_soql_value( username )

        return cls._select_user_query(
            where_clause = f"Username = '{ escaped_username }'"
        )

    @classmethod
    def by_email( cls, email: str ) -> str:
        escaped_email = cls._escape_soql_value( email )

        return cls._select_user_query(
            where_clause = f"Email = '{ escaped_email }'"
        )

    @classmethod
    def by_id( cls, user_id: str ) -> str:
        escaped_user_id = cls._escape_soql_value( user_id )

        return cls._select_user_query(
            where_clause = f"Id = '{ escaped_user_id }'"
        )

    @classmethod
    def _select_user_query( cls, where_clause: str ) -> str:
        fields = ", ".join( cls.USER_FIELDS )

        return f"SELECT { fields } FROM User WHERE { where_clause } LIMIT 1"

    @staticmethod
    def _escape_soql_value( value: str ) -> str:
        return value.replace( "\\", "\\\\" ).replace( "'", "\\'" )