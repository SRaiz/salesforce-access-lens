class Validation:
    """
    Common validation utilities used across the application.
    """

    @staticmethod
    def validate_required( field_name: str, value: str ) -> None:
        
        if value is None or not value.strip():
            raise ValueError( f"{ field_name } cannot be empty.")