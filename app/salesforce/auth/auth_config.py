from dataclasses import dataclass

@dataclass( frozen = True )
class AuthConfig:
    
    """
    Holds Salesforce JWT authentication configuration.

    This class does not read environment variables.
    It only stores the values required for authentication.
    """
    consumer_key        : str
    username            : str
    login_url           : str
    private_key_path    : str