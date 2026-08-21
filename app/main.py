from dotenv import load_dotenv

from app.config import ConfigFactory, Environment
from app.services import AccessLensService
from app.bootstrap import AccessLensServiceFactory
from app.salesforce.auth import AuthConfig
from app.salesforce.domain import SalesforceConfig


def main() -> None:
    # Load environment variables.
    load_dotenv()

    # Build application configuration.
    environment                 : Environment = Environment()
    config_factory              : ConfigFactory = ConfigFactory( environment )

    auth_config                 : AuthConfig = config_factory.create_auth_config()
    salesforce_config           : SalesforceConfig = config_factory.create_salesforce_config()

    # Build access lens service factory
    access_lens_service_factory : AccessLensServiceFactory = AccessLensServiceFactory(
        auth_config         = auth_config,
        salesforce_config   = salesforce_config
    )

    # Build access lens service
    access_lens_service         : AccessLensService = access_lens_service_factory.create()
    print( "\nSalesforce Access Lens initialized successfully!" )

    # Analyze the Salesforce user's access.
    analysis = access_lens_service.analyze_user(
        auth_config.username
    )

    print( "\nAccess Analysis completed successfully!" )
    print( analysis )

    # Analyze the Salesforce user access for account object
    account_explanation = analysis.explain_object_access(
        "Account"
    )
    print( "\n================ Account Access Explanation ================" )
    print( account_explanation )

    unknown_object_explanation = analysis.explain_object_access(
        "UnknownObject"
    )
    print( "\n================ Unknown Object Explanation ================" )
    print( unknown_object_explanation )

    print( "\n================ Account Permission Sources ================")
    for source in account_explanation.sources:
        print( source )

    # Analyze the Salesforce user access for account object field AnnualRevenue
    account_annual_revenue_explanation = (
        analysis.explain_field_access(
            "Account",
            "AnnualRevenue"
        )
    )
    print( "\n======== Account.AnnualRevenue Field Access Explanation ========" )
    print( account_annual_revenue_explanation )


    unknown_field_explanation = (
        analysis.explain_field_access(
            "UnknownObject",
            "UnknownField"
        )
    )
    print( "\n========== Unknown Object's Field Explanation ==========" )
    print( unknown_field_explanation )


    print( "\n========== Account.AnnualRevenue Permission Sources ==========")
    for source in account_annual_revenue_explanation.sources:
        print( source )


if __name__ == "__main__":
    main()