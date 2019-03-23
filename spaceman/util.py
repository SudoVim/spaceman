"""
functionality of the spaceman utility
"""

import os
import sys
import argparse
import importlib

def list_deployments(args):
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
                            if hasattr(deployment, 'NAME'):
                                found_deployments.append(deployment)

                            else:
                                print(
                                    "File %s deployment %s lacks NAME field" % (
                                        filepath,
                                        deployment.__name__,
                                    ),
                                    file=sys.stderr,
                                )

    if not found_deployments:
        print("Found nothing!")

    for deployment in found_deployments:
        print(deployment.NAME)

    return 0

def main(argv):
    """ main function """
    parser = argparse.ArgumentParser(
        description="main ingress into spaceman functionality",
    )

    subparser = parser.add_subparsers(help="sub-command help")

    parser_list = subparser.add_parser('list', help='list available deployments')
    parser_list.set_defaults(func=list_deployments)

    args = parser.parse_args(argv)
    if not hasattr(args, 'func'):
        print("Sub-command required.", file=sys.stderr)
        parser.print_help()
        return -1

    return args.func(args)
