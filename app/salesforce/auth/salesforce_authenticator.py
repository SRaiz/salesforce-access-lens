from app.salesforce.auth import OAuthClient
from app.salesforce.domain import SalesforceAuthSession


class SalesforceAuthenticator:
    
    def __init__(
        self, 
        oauth_client: OAuthClient
    ) -> None:
        self._oauth_client = oauth_client
        
    def authenticate( self ) -> SalesforceAuthSession:
        """
        Authenticates with Salesforce and returns an authenticated session.
        """
        response_body = self._oauth_client.exchange_jwt_for_token()
        
        return SalesforceAuthSession(
            access_token    = response_body[ "access_token" ], 
            instance_url    = response_body[ "instance_url" ], 
            token_type      = response_body.get( "token_type", "Bearer" )
        )