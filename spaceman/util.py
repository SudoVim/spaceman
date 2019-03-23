"""
functionality of the spaceman utility
"""

import sys
import argparse

from .discovery import find_deployments

def list_deployments(args):
    """
        handler for ``list`` subcommand
    """
    found_deployments = find_deployments()

    if not found_deployments:
        print("Found nothing!")

    for deployment in found_deployments:
        print(deployment.NAME)

    return 0

def run_deployment(args):
    """
        handler for ``run`` subcommand
    """
    found_deployments = find_deployments(args.name)
    if not found_deployments:
        print("Deployment", args.name, "not found!", file=sys.stderr)
        return -1

    if len(found_deployments) > 1:
        print(
            "Found multiple deployments with name %s." % args.name,
            file=sys.stderr,
        )
        return -1

    return found_deployments[0]().run()

def main(argv):
    """ main function """
    parser = argparse.ArgumentParser(
        description="main ingress into spaceman functionality",
    )

    subparser = parser.add_subparsers(help="sub-command help")

    parser_list = subparser.add_parser('list', help='list available deployments')
    parser_list.set_defaults(func=list_deployments)

    parser_run = subparser.add_parser('run', help='run given deployment')
    parser_run.add_argument(
        'name', help='name of deployment to run',
    )
    parser_run.set_defaults(func=run_deployment)

    args = parser.parse_args(argv)
    if not hasattr(args, 'func'):
        print("Sub-command required.", file=sys.stderr)
        parser.print_help()
        return -1

    return args.func(args)
