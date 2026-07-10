class FieldPermissionQueries:
    """
    Builds SOQL queries related to FieldPermissions records.
    """

    FIELD_PERMISSION_FIELDS = [
        "Id",
        "ParentId",
        "SObjectType",
        "Field",
        "PermissionsRead",
        "PermissionsEdit",
    ]

    @classmethod
    def by_parent_id( cls, parent_id: str ) -> str:
        escaped_parent_id = cls._escape_soql_value( parent_id )

        return cls._select_field_permission_query(
            where_clause = f"ParentId = '{ escaped_parent_id }'"
        )

    @classmethod
    def by_parent_ids(cls, parent_ids: set[ str ]) -> str:
        if not parent_ids:
            raise ValueError(
                "At least one parent Permission Set Id must be provided."
            )

        escaped_parent_ids = ", ".join(
            f"'{ cls._escape_soql_value( parent_id )}'"
            for parent_id in sorted( parent_ids )
        )

        return cls._select_field_permission_query(
            where_clause = f"ParentId IN ({ escaped_parent_ids })"
        )

    @classmethod
    def _select_field_permission_query( cls,  where_clause: str ) -> str:
        fields = ", ".join(cls.FIELD_PERMISSION_FIELDS)

        return (
            "SELECT "
            f"{ fields } "
            "FROM FieldPermissions "
            f"WHERE { where_clause }"
        )

    @staticmethod
    def _escape_soql_value( value: str ) -> str:
        return value.replace( "\\", "\\\\" ).replace( "'", "\\'" )