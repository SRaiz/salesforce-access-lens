from app.services import AccessLensService
from app.salesforce.auth import (
    AuthConfig,
    JWTBuilder,
    OAuthClient,
    SalesforceAuthenticator,
)
from app.salesforce.client import SalesforceClient
from app.salesforce.domain import (
    SalesforceAuthSession,
    SalesforceConfig,
)
from app.salesforce.query import SoqlQueryExecutor
from app.salesforce.repositories import (
    UserRepository,
    ProfileRepository,
    PermissionSetAssignmentRepository,
    PermissionSetRepository,
    ObjectPermissionRepository,
    FieldPermissionRepository,
)


class AccessLensServiceFactory:
    """
    Constructs a fully configured AccessLensService.

    The factory stores the configuration required for application
    construction. Salesforce authentication and dependency creation
    happen explicitly inside the create method.
    """

    def __init__(
        self,
        auth_config        : AuthConfig,
        salesforce_config  : SalesforceConfig,
    ) -> None:
        self._auth_config        = auth_config
        self._salesforce_config  = salesforce_config

    def create( self ) -> AccessLensService:
        """
        Authenticates with Salesforce and constructs all dependencies
        required by AccessLensService.
        """

        salesforce_auth_session: SalesforceAuthSession = self._authenticate()

        # Build the Salesforce API infrastructure.
        salesforce_client: SalesforceClient = SalesforceClient(
            session = salesforce_auth_session,
            config  = self._salesforce_config,
        )

        query_executor: SoqlQueryExecutor = SoqlQueryExecutor( salesforce_client )

        # Build repositories.
        user_repository                         = UserRepository( query_executor )
        profile_repository                      = ProfileRepository( query_executor )
        permission_set_assignment_repository    = PermissionSetAssignmentRepository( query_executor )
        permission_set_repository               = PermissionSetRepository( query_executor )
        object_permission_repository            = ObjectPermissionRepository( query_executor )
        field_permission_repository             = FieldPermissionRepository( query_executor )

        # Build the application service.
        access_lens_service = AccessLensService(
            user_repository                         = user_repository, 
            profile_repository                      = profile_repository, 
            permission_set_assignment_repository    = permission_set_assignment_repository, 
            permission_set_repository               = permission_set_repository,
            object_permission_repository            = object_permission_repository,
            field_permission_repository             = field_permission_repository,
        )
        
        return access_lens_service

    def _authenticate(self) -> SalesforceAuthSession:
        """
        Authenticates with Salesforce using the configured JWT
        Bearer Flow and returns an authenticated session.
        """

        # Build the Salesforce authentication flow.
        jwt_builder                 : JWTBuilder = JWTBuilder( self._auth_config )
        oauth_client                : OAuthClient = OAuthClient( jwt_builder )

        salesforce_authenticator    : SalesforceAuthenticator = SalesforceAuthenticator( oauth_client )
        salesforce_auth_session     : SalesforceAuthSession = salesforce_authenticator.authenticate()

        return salesforce_auth_session