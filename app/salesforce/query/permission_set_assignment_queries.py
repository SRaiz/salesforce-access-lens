class PermissionSetAssignmentQueries:
    """
    Builds SOQL queries related to Permission Set Assignment records.
    """

    PERMISSION_SET_ASSIGNMENT_FIELDS = [
        "Id",
        "AssigneeId",
        "PermissionSetId",
    ]

    @classmethod
    def by_user_id( cls, user_id: str ) -> str:
        escaped_user_id = cls._escape_soql_value( user_id )

        return cls._select_permission_set_assignment_query(
            where_clause = f"AssigneeId = '{ escaped_user_id }'"
        )

    @classmethod
    def _select_permission_set_assignment_query( cls, where_clause: str ) -> str:
        fields = ", ".join( cls.PERMISSION_SET_ASSIGNMENT_FIELDS )

        return (
            "SELECT "
            f"{ fields } "
            "FROM PermissionSetAssignment "
            f"WHERE { where_clause }"
        )

    @staticmethod
    def _escape_soql_value( value: str ) -> str:
        return value.replace( "\\", "\\\\" ).replace( "'", "\\'" )