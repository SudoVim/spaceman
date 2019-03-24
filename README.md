# spaceman

Infrastructure for launching services, linking them together, and testing their
connections.

## Preface

I love starting projects and playing around with them. The issue that I face is
that there's a lot of infrastructure that I need to set up to even get them up
and running for development purposes.

## Deployments

A deployment is a service that can be launched for a project. This idea is meant
to be flexible in spaceman. For instance, for development purposes, a deployment
will be launched with its own unique directory to store its data. For production
purposes, it will be launched with a static location to store its data. For
testing purposes, its data will just live within the container itself.

Spaceman itself will provide a set of deployment types that can be extended by
creating a `.spaceman` directory in your project. Each of these directories
will be discovered, and all `*.py` files will be loaded to look for potential
deployments. One such deployment could be:

```python
class MyMongoDBDeployment(object):
    """
        MongoDB spaceman deployment for My project
    """

    NAME = 'pyproject-mongodb'
    BASE = 'MongoDBDeployment'

    DOCKER_TAG = '3.4.20'

SPACEMAN_DEPLOYMENTS = [
    MyMongoDBDeployment,
]
```

In this case, your project is using the `MongoDBDeployment` deployment as a base
class. The spaceman project handles all of the type creation.

**Note:** - This project is still under construction and is not yet ready for use.
