from app.salesforce.client import SalesforceClient

class SoqlQueryExecutor:
    
    """
    Executes SOQL queries using the Salesforce client.

    This class does not build business-specific queries.
    It only receives a SOQL query string and executes it.
    """
    def __init__(
        self, 
        client: SalesforceClient
    ) -> None:
        self._client = client
        
    def execute( self, query: str ):
        """
        Executes a SOQL query against Salesforce.
        """
        if not query or not query.strip():
            raise ValueError( "Salesforce queries can't be balnk or empty." )
        
        return self._client.get(
            endpoint    = "query", 
            params      = { "q" : f"{query}" }
        )        