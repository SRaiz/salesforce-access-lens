from app.utils import Validation

class SalesforceUser():
    """
    Represents a Salesforce User within the Salesforce Access Lens domain.
    """
    
    def __init__(
        self, 
        user_id     : str, 
        name        : str, 
        username    : str, 
        email       : str, 
        profile_id  : str, 
        is_active   : bool, 
        user_type   : str
    ):
        Validation.validate_required( "user_id", user_id )
        Validation.validate_required( "name", name )
        Validation.validate_required( "username", username )
        Validation.validate_required( "email", email )
        Validation.validate_required( "profile_id", profile_id )
        Validation.validate_required( "user_type", user_type )
        
        self._user_id           = user_id
        self._name              = name
        self._username          = username
        self._email             = email
        self._profile_id        = profile_id
        self._is_active         = is_active
        self._user_type         = user_type
        
    @property
    def user_id( self ) -> str:
        return self._user_id

    @property
    def name( self ) -> str:
        return self._name

    @property
    def username( self ) -> str:
        return self._username

    @property
    def email( self ) -> str:
        return self._email

    @property
    def profile_id( self ) -> str:
        return self._profile_id

    @property
    def is_active( self ) -> bool:
        return self._is_active

    @property
    def user_type( self ) -> str:
        return self._user_type

    @property
    def profile( self ):
        return self._profile

    def is_internal_user( self ) -> bool:
        return self._user_type == "Standard"

    def is_active_user( self ) -> bool:
        return self._is_active
        
    def __repr__( self ) -> str:
        return (
            "\n"
            f"User ID       : { self.user_id }\n"
            f"Username      : { self.username }\n"
            f"Profile Id    : { self.profile_id }\n"
            f"Is Active     : { self.is_active }\n"
        )
        
    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, SalesforceUser ):
            return NotImplemented
        
        return self._user_id == other._user_id
    
    def __hash__( self ) -> int:
        return hash( self._user_id )