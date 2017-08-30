"""
Util classes/methods for managing different hardware platforms supported
by wlan_exp and the 802.11 ref design
"""

registered_platforms = []

class WlanExpPlatform(object):
    """Container class describing wlan_exp hardware platforms"""

    name = None
    sn_regexp = None
    sn_str_fmt = None
    # TODO: add property to track per-platform node object class/factory

    def __init__(self, name, sn_regexp, sn_str_fmt):
        self.name = name
        self.sn_regexp = sn_regexp
        self.sn_str_fmt = sn_str_fmt

    def __repr__(self):
        return 'wlan_exp Platform {0} ({1})'.format(self.name, self.get_serial_number_str(12345))

    def get_serial_number_str(self, serial_num_int):
        """ Returns serial number string for numeric serial number
        serial_num_int. This method probably belongs in the top-level
        node object. It's here for now as we work on platform code.
        """
        return self.sn_str_fmt.format(serial_num_int)

    def check_serial_numer(self, sn_str):
        """
        Returns true if sn_str is a valid serial number for this platform
        Platforms can override this method if they need something more than 
         the regexp check implemented here
        """
        if(self.get_serial_number(sn_str)):
            return True
        else:
            return False

    def get_serial_number(self, sn_str):
        """
        Returns the numeric part of the serial number in sn_str. This is probably
        a temporary method that will be replaced by a better platform-agnostic scheme
        when the transport.node() init and node discovery processes are imrpvoed
        """
        import re

        expr = re.compile(self.sn_regexp)
        m = expr.match(sn_str)

        if(m and 'sn' in m.groupdict()):
            # Returns tuple (a,b)
            #  a: serial number int
            #  b: serial number string in preferred format
            sn_int = int(m.group('sn'))
            return (sn_int, self.get_serial_number_str(sn_int))

        return None

def register_platform(new_platform):
    """ Adds new platform description to the global list of registered platforms"""

    registered_platforms.append(new_platform)

def lookup_platform_by_serial_num(serial_num):
    """ Checks if serial_num is valid serial number for any registered platforms
        If so returns matching WlanExpPlatform object
    """
    
    import re

    for p in registered_platforms:
        if(p.check_serial_numer(serial_num)):
            return p

    return None


def get_serial_number(serial_num):
    """ Temporary method to replace old wlan_exp.transport.util.get_serial_num() helper
        This is a half-step towards a more general platform structure
    """
    p = lookup_platform_by_serial_num(serial_num)
    if(p):
        return p.get_serial_number(serial_num)
    else:
        raise Exception('No platform found for serial number {0}'.format(serial_num))
