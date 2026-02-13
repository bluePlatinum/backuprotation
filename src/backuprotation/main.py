import argparse
import os
import sys
import logging

from backuprotation import PROJECTNAME, VERSION

logger = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="backuprotation",
        description="Rotates backups for you.",
        epilog=f"{PROJECTNAME} {VERSION}"
    )

    parser.add_argument(
        "path",
        help="The path of the backup directory."
    )

    parser.add_argument(
        "-n", "--number",
        action="store",
        default=10,
        type=int,
        help="The number of backups to keep."
    )

    parser.add_argument(
        "-f", "--files",
        action="store_true",
        help=f"If this option is selected {PROJECTNAME} looks for files "
             f"instead of directories to rotate."
    )

    parser.add_argument(
        "-fd", "--files-and-directories",
        action="store_true",
        help=f"If this option is selected {PROJECTNAME} looks both for files "
             f"and directories to rotate."
    )

    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="dry-run: do not delete anything"
    )

    return parser.parse_args(args)


def discover(path, dirs=True, files=False):
    discovered = list()
    for f in os.listdir(os.path.abspath(path)):
        f = os.path.join(path, f)
        if dirs and os.path.isdir(f):
            discovered.append(f)
        if files and os.path.isfile(f):
            discovered.append(f)

    return sorted(discovered, key=lambda d: os.path.getmtime(d))


def rotate(discovered, number, dry_run):
    if len(discovered) <= number:
        return

    scheduled = discovered[:len(discovered) - number]

    for element in scheduled:
        if os.path.isfile(element):
            logger.info(f"deleting file {element}")
            if not dry_run:
                os.remove(element)

        else:
            logger.info(f"deleting directory {element}")
            if not dry_run:
                os.rmdir(element)


def main():
    args = parse_args(sys.argv[1:])

    if args.files:
        dirs = False
        files = True
    elif args.files_and_directories:
        dirs = True
        files = True
    else:
        dirs = True
        files = False

    discovered = discover(args.path, dirs, files)

    rotate(discovered, args.number, args.dry_run)
