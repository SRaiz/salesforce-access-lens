import requests

from app.salesforce.domain import SalesforceConfig, SalesforceAuthSession

class SalesforceClient:
    
    """
    Low-level client responsible for making authenticated
    HTTP requests to Salesforce REST APIs.
    """
    def __init__(
        self, 
        config  : SalesforceConfig, 
        session : SalesforceAuthSession
    ) -> None:
        self._config     = config
        self._session    = session
        
    @property
    def base_url( self ) -> str:
        return f"{ self._session.instance_url }/services/data/{ self._config.api_version }"
    
    @property
    def headers( self ) -> dict[ str, str ]:
        return{
            "Authorization" : f"{ self._session.token_type } { self._session.access_token }", 
            "Content-Type"  : "application/json"
        }
        
    def get( self, endpoint: str, params: dict[ str, str ] ) -> dict:
        """
        Sends an authenticated GET request to Salesforce.
        """
        url = f"{ self.base_url }/{ endpoint.lstrip('/') }"
        
        response = requests.get(
            url         = url, 
            headers     = self.headers, 
            params      = params, 
            timeout     = 30
        )
        
        response.raise_for_status()
        return response.json()
        