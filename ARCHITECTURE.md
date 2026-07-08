# Salesforce Access Lens Architecture

## Layers

Configuration
- Environment
- ConfigFactory

Authentication
- AuthConfig
- JWTBuilder
- OAuthClient
- SalesforceAuthenticator
- SalesforceAuthSession

Communication
- SalesforceClient
- SoqlQueryExecutor

Future
- Repositories
- Services
- MCP Server