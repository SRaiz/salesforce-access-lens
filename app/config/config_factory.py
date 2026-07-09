from app.salesforce.auth import AuthConfig
from app.salesforce.domain import SalesforceConfig
from app.config import Environment

class ConfigFactory:
    
    def __init__(
        self, 
        environment: Environment
    ) -> None:
        self._environment = environment
        
    def create_auth_config( self ) -> AuthConfig:
        return AuthConfig(
            consumer_key        = self._environment.get_required( "SF_CONSUMER_KEY" ), 
            username            = self._environment.get_required( "SF_USERNAME" ), 
            login_url           = self._environment.get_required( "SF_LOGIN_URL" ),
            private_key_path    = self._environment.get_required( "SF_PRIVATE_KEY_PATH" ),
        )
        
    def create_salesforce_config( self ) -> SalesforceConfig:
        return SalesforceConfig(
            api_version = self._environment.get_required( "SF_API_VERSION" )
        )