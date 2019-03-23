"""
deployment base classes
"""

class Deployment(object):
    """
        base class for all deployment classes
    """

    NAME = None

    @classmethod
    def check(cls):
        """
            check deployment against best practices
        """
        return True

    def run(self):
        """
            method to run the deployment
        """
        raise NotImplementedError
