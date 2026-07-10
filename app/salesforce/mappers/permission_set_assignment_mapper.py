from app.salesforce.domain import PermissionSetAssignment

class PermissionSetAssignmentMapper:
    """
    Maps Salesforce PermissionSetAssignment records into domain entities.
    """

    @staticmethod
    def from_record( record: dict ) -> PermissionSetAssignment:
        """
        Converts a Salesforce PermissionSetAssignment record into a domain entity.
        """

        return PermissionSetAssignment(
            assignment_id     = record[ "Id" ],
            assignee_id       = record[ "AssigneeId" ],
            permission_set_id = record[ "PermissionSetId" ],
        )