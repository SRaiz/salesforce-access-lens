from dataclasses import dataclass

@dataclass
class SalesforceConfig:
    
    """
    Holds general Salesforce API configuration.

    This is separate from authentication because these values
    are needed after authorization / authentications as well.
    """
    api_version: str = "v65.0"