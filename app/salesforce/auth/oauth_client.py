import requests
from app.salesforce.auth import JWTBuilder

# Constants
SF_JWT_CONTENT_TYPE = "application/x-www-form-urlencoded"
SF_JWT_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"

class OAuthClient:
    """
    Client responsible for calling Salesforce OAuth endpoints.
    """

    def __init__(
        self,
        jwt_builder: JWTBuilder
    ) -> None:
        self._jwt_builder = jwt_builder

    def exchange_jwt_for_token( self ) -> dict:
        """
        Exchanges a signed JWT assertion for a Salesforce access token response.
        """

        jwt_assertion = self._jwt_builder.build()

        response = requests.post(
            url         = self._token_url,
            data        = self._create_token_payload( jwt_assertion ),
            headers     = { "Content-Type": SF_JWT_CONTENT_TYPE },
            timeout     = 30,
        )

        response.raise_for_status()
        return response.json()

    def _create_token_payload(
        self,
        jwt_assertion: str
    ) -> dict[ str, str ]:
        return {
            "grant_type"    : SF_JWT_GRANT_TYPE,
            "assertion"     : jwt_assertion,
        }

    @property
    def _token_url(self) -> str:
        return f"{ self._jwt_builder.auth_config.login_url }/services/oauth2/token"