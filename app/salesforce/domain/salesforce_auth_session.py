from dataclasses import dataclass

@dataclass( frozen = True )
class SalesforceAuthSession:
    
    """
    Represents an authenticated Salesforce session.

    This object is returned after successful authentication
    and is later used by Salesforce clients to make API calls.
    """
    access_token    : str
    instance_url    : str
    token_type      : str = "Bearer"