"""
MongoDB Deployment
"""

from .docker import DockerDeployment

class MongoDBDeployment(DockerDeployment):
    """
        base class for MongoDB deployments
    """

    DOCKER_IMAGE = 'mongo'
