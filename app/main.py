from dotenv import load_dotenv

from app.config import ConfigFactory, Environment
from app.services import AccessLensService
from app.salesforce.auth import (
    AuthConfig,
    JWTBuilder,
    OAuthClient,
    SalesforceAuthenticator
)
from app.salesforce.client import SalesforceClient
from app.salesforce.domain import SalesforceAuthSession, SalesforceConfig
from app.salesforce.query import SoqlQueryExecutor
from app.salesforce.repositories import (
    UserRepository,
    ProfileRepository,
    PermissionSetAssignmentRepository,
    PermissionSetRepository,
    ObjectPermissionRepository,
    FieldPermissionRepository
)


def main() -> None:
    # Load environment variables.
    load_dotenv()

    # Build application configuration.
    environment                 : Environment = Environment()
    config_factory              : ConfigFactory = ConfigFactory( environment )
    
    auth_config                 : AuthConfig = config_factory.create_auth_config()
    salesforce_config           : SalesforceConfig = config_factory.create_salesforce_config()

    # Build the Salesforce authentication flow.
    jwt_builder                 : JWTBuilder = JWTBuilder( auth_config )
    oauth_client                : OAuthClient = OAuthClient( jwt_builder )

    salesforce_authenticator    : SalesforceAuthenticator = SalesforceAuthenticator( oauth_client )
    salesforce_auth_session     : SalesforceAuthSession = salesforce_authenticator.authenticate()

    print( "Authentication Successful!" )
    print(
        {
            "Instance URL"  : salesforce_auth_session.instance_url,
            "Token Type"    : salesforce_auth_session.token_type,
        }
    )

    # Build the Salesforce API infrastructure.
    salesforce_client: SalesforceClient = SalesforceClient(
        session = salesforce_auth_session,
        config  = salesforce_config,
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

    # Analyze the Salesforce user's access.
    analysis = access_lens_service.analyze_user(
        auth_config.username
    )

    print( "\nAccess Analysis completed successfully!" )
    print( analysis )
    
    account_explanation = analysis.explain_object_access(
        "Account"
    )

    print( "\n================ Account Access Explanation ================" )
    print( account_explanation )

    unknown_object_explanation = analysis.explain_object_access(
        "UnknownObject"
    )

    print( "\n================ Unknown Object Explanation ================" )
    print( unknown_object_explanation )
    
    print( "\n================ Account Permission Sources ================")

    for source in account_explanation.sources:
        print( source )


if __name__ == "__main__":
    main()