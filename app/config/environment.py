import os

class Environment:
    """
    Reads environment variables for the application.
    """

    def get_required(
        self, 
        key: str
    ) -> str:
        value = os.getenv( key )

        if value is None or not value.strip():
            raise ValueError( f"Missing required environment variable: {key}" )

        return value.strip()

    def get_optional(
        self,
        key: str,
        default: str | None = None
    ) -> str | None:
        value = os.getenv( key )

        if value is None or not value.strip():
            return default

        return value.strip()