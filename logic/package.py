"""
Module Summary
Contains classes for representing package objects. 
Module Details
"""

class Package:
    """
    Class Summary
    This class contains the base information about a package

    Class Details
    Package: name, id, pid
    """

    # Class Constructor
    def __init__(self, name):
        """
        Function Summary

        """
        self.name = name
        self.id = 0
        self.pid = 0

    # Class deconstructor
    def __del__(self):
        """
        Function Summary
        
        """
        pass

    
