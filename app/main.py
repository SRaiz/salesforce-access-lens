from dotenv import load_dotenv
from app.config import Environment, ConfigFactory
from app.salesforce.auth import AuthConfig, JWTBuilder, OAuthClient, SalesforceAuthenticator
from app.salesforce.client import SalesforceClient
from app.salesforce.models import SalesforceAuthSession, SalesforceConfig

def main() -> None:
    
    # We build the environment first
    load_dotenv()
    environment         : Environment = Environment()
    
    # Then post getting the environment lets build the auth_config and sf_config
    config              : ConfigFactory             = ConfigFactory( environment )
    auth_config         : AuthConfig                = config.create_auth_config()
    
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

if __name__ == "__main__":
    main()