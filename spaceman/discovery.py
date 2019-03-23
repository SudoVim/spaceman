"""
module for deployment discovery
"""

import os
import logging
import importlib

from . import deployments

logger = logging.getLogger("spaceman.discovery")

def find_deployments(name=None):
    """
        handler for ``list`` subcommand
    """
    # Find .spaceman directories
    spaceman_dirs = []
    for root, dirs, files in os.walk('.'):
        if '.spaceman' in dirs:
            spaceman_dirs.append(os.path.join(root, '.spaceman'))

    found_deployments = []
    for spaceman_dir in spaceman_dirs:
        for root, dirs, files in os.walk(spaceman_dir):
            for fname in files:
                if fname.endswith(".py"):
                    filepath = os.path.join(root, fname)
                    module = importlib.machinery.SourceFileLoader(
                        'module',
                        filepath,

                    ).load_module()

                    if hasattr(module, 'SPACEMAN_DEPLOYMENTS'):
                        for deployment in module.SPACEMAN_DEPLOYMENTS:
                            if not hasattr(deployment, 'NAME'):
                                logger.error(
                                    "File %s deployment %s lacks NAME field" % (
                                        filepath,
                                        deployment.__name__,
                                    ),
                                )
                                continue

                            if name is not None and deployment.NAME != name:
                                continue

                            if not hasattr(deployment, 'BASE'):
                                logger.error(
                                    "File %s deployment %s lacks BASE field" % (
                                        filepath,
                                        deployment.__name__,
                                    ),
                                )
                                continue

                            if not hasattr(deployments, deployment.BASE):
                                logger.error(
                                    "File %s deployment %s BASE %s not found" % (
                                        filepath,
                                        deployment.__name__,
                                        deployment.BASE,
                                    ),
                                )
                                continue

                            bound_deployment = type(
                                "Bound%s" % deployment.__name__,
                                (deployment, getattr(deployments, deployment.BASE)),
                                {'SOURCE_DIR': root},
                            )

                            if not bound_deployment.check():
                                continue

                            found_deployments.append(bound_deployment)

    return found_deployments
