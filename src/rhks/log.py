
def print_error( msg ):
    """print error messgae
    """
    print "ERROR:   " + msg

def print_info( msg ):
    """print info level message
    """
    print "INFO:    " + msg

def print_warn( msg ):
    """print warning level message
    """
    print "WARNING: " + msg

def print_debug( msg ):
    """print debug level message
    """
    if not msg == None:
        print "DEBUG:   " + msg
    else:
        print "DEBUG:   none"
