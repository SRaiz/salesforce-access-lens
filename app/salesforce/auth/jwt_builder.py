import jwt
from datetime import datetime, timedelta, timezone
from app.salesforce.auth.auth_config import AuthConfig

# Constants
JWT_ALGORITHM               = "RS256"
JWT_EXPIRATION_MINUTES      = 3

class JWTBuilder:
    """
    Builds a signed JWT assertion for Salesforce JWT Bearer Flow.
    """
    
    def __init__( self, auth_config: AuthConfig ) -> None:
        self._auth_config = auth_config

    def build( self ) -> str:
        """
        Builds and returns a signed JWT assertion.
        """
        private_key = self._load_private_key()
        jwt_payload = self._create_jwt_payload()
        
        return jwt.encode(
            payload     = jwt_payload, 
            key         = private_key, 
            algorithm   = JWT_ALGORITHM
        )
        
    @property
    def auth_config( self ) -> AuthConfig:
        return self._auth_config
    
    def _load_private_key( self ) -> str:
        """
        Loads the private key used to sign the JWT.
        """
        with open( self._auth_config.private_key_path, "r", encoding = "utf-8" ) as key_file:
            return key_file.read()
        
    def _create_jwt_payload( self ) -> dict:
        return {
            "iss"   : self._auth_config.consumer_key, 
            "sub"   : self._auth_config.username, 
            "aud"   : self._auth_config.login_url, 
            "exp"   : datetime.now( timezone.utc ) + timedelta( minutes = JWT_EXPIRATION_MINUTES )
        }