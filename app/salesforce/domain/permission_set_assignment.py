from app.utils import Validation

class PermissionSetAssignment:
    """
    Represents the assignment of a Permission Set to a Salesforce User.
    """

    def __init__(
        self,
        assignment_id       : str,
        assignee_id         : str,
        permission_set_id   : str,
    ) -> None:
        Validation.validate_required( "assignment_id", assignment_id )
        Validation.validate_required( "assignee_id", assignee_id )
        Validation.validate_required( "permission_set_id", permission_set_id )

        self._assignment_id         = assignment_id
        self._assignee_id           = assignee_id
        self._permission_set_id     = permission_set_id

    @property
    def assignment_id( self ) -> str:
        return self._assignment_id

    @property
    def assignee_id( self ) -> str:
        return self._assignee_id

    @property
    def permission_set_id( self ) -> str:
        return self._permission_set_id

    def belongs_to_user( self, user_id: str ) -> bool:
        return self._assignee_id == user_id

    def references_permission_set( self, permission_set_id: str ) -> bool:
        return self._permission_set_id == permission_set_id

    def __repr__( self ) -> str:
        return (
            "\n"
            f"Assignment Id       : { self.assignment_id }\n"
            f"Assignee Id         : { self.assignee_id }\n"
            f"Permission Set Id   : { self.permission_set_id }\n"
        )

    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, PermissionSetAssignment ):
            return NotImplemented

        return self._assignment_id == other._assignment_id

    def __hash__( self ) -> int:
        return hash( self._assignment_id )