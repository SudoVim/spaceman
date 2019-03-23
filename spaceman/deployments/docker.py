"""
docker deployment base class
"""

import sys
import subprocess

from .base import Deployment

class DockerDeployment(Deployment):
    """
        base class for all docker deployments
    """

    DOCKER_IMAGE = None
    DOCKER_TAG = 'latest'

    @classmethod
    def check(cls):
        if cls.DOCKER_IMAGE is None:
            print(
                "Deployment %s doesn't have DOCKER_IMAGE defined" % (
                    cls.NAME,
                ),
                file=sys.stderr,
            )
            return False

        return True

    def run(self):
        """
            method to run the docker deployment
        """
        code = subprocess.call(
            [
                'docker', 'run', '--rm', '-ti',
                "%s:%s" % (self.DOCKER_IMAGE, self.DOCKER_TAG),
            ],
        )
