
class Error(Exception):
    """Base class for exceptions in rhks module
    """
    pass

class DuplicationError(Error):
    """Exception raised for errors on duplicated items
    """

    def __init__(self, msg):
        """
        
        Arguments:
        - `msg`:
        """
        self.msg = msg
        
class InvalidCommandError( Error):
    """Exception raised for errors on invalid command
    """

    def __init__(self, msg ):
        """

        Arguments:
        - `msg`:
        """
        self.msg = msg
        
