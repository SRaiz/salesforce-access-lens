from dotenv import load_dotenv
from app.config import Environment, ConfigFactory
from app.salesforce.auth import AuthConfig, JWTBuilder, OAuthClient, SalesforceAuthenticator
from app.salesforce.client import SalesforceClient
from app.salesforce.domain import SalesforceAuthSession, SalesforceConfig
from app.salesforce.repositories import (
    UserRepository, 
    ProfileRepository, 
    PermissionSetRepository, 
    PermissionSetAssignmentRepository
)
from app.salesforce.query import SoqlQueryExecutor

def main() -> None:
    
    # We build the environment first
    load_dotenv()
    environment         : Environment = Environment()
    
    # Then post getting the environment lets build the auth_config and sf_config
    config              : ConfigFactory             = ConfigFactory( environment )
    auth_config         : AuthConfig                = config.create_auth_config()
    salesforce_config   : SalesforceConfig          = config.create_salesforce_config()
    
    # Lets create the jwt using jwt builder
    jwt_builder         : JWTBuilder                = JWTBuilder( auth_config )
    
    # Lets create the oauth client now using the jwt assertion
    oauth_client        : OAuthClient               = OAuthClient( jwt_builder )
    
    # Lets create the salesforce authenticator for authenticaion
    sf_authenticator    : SalesforceAuthenticator   = SalesforceAuthenticator( oauth_client )
    
    # Finally lets call the authenticate method from sf_authenticator to get SalesorceAuthSession
    sf_auth_session     : SalesforceAuthSession     = sf_authenticator.authenticate()
    
    if sf_auth_session:
        print( "Authentication Successful!" )
        print({
            "Instance URL"  : sf_auth_session.instance_url, 
            "Token Type"    : sf_auth_session.token_type
        })
        
    salesforce_client = SalesforceClient(
        session = sf_auth_session,
        config  = salesforce_config
    )
    
    query_executor      : SoqlQueryExecutor         = SoqlQueryExecutor( salesforce_client )
    user_repository     : UserRepository            = UserRepository( query_executor )

    user = user_repository.find_by_username( auth_config.username )

    print( "User fetched successfully!" )
    print( user )
    
    profile_repository  : ProfileRepository         = ProfileRepository( query_executor )
    profile = profile_repository.find_by_id( user.profile_id )
    
    print( "Profile fetched successfully!" )
    print( profile )
    
    permission_set_assignment_repository = PermissionSetAssignmentRepository( query_executor )
    permission_set_repository = PermissionSetRepository( query_executor )

    permission_set_assignments = permission_set_assignment_repository.find_by_user_id(
        user.user_id
    )

    permission_set_ids = {
        assignment.permission_set_id
        for assignment in permission_set_assignments
    }

    permission_sets = permission_set_repository.find_by_ids(
        permission_set_ids
    )

    print( "Permission Set Assignments fetched successfully!" )
    print( f"Assignment Count: { len( permission_set_assignments )}" )

    print( "Permission Sets fetched successfully!" )
    print( f"Permission Set Count: { len( permission_sets )}" )

    profile_owned_permission_sets = [
        permission_set
        for permission_set in permission_sets
        if permission_set.is_profile_owned()
    ]

    assigned_permission_sets = [
        permission_set
        for permission_set in permission_sets
        if permission_set.is_standalone_permission_set()
    ]

    print( "\n================ Profile-owned Permission Sets ================\n" )

    for permission_set in profile_owned_permission_sets:
        print( permission_set )

    print( "\n================ Explicitly Assigned Permission Sets ================\n" )

    for permission_set in assigned_permission_sets:
        print( permission_set )

if __name__ == "__main__":
    main()