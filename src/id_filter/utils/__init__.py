"""
A package contains necessary methods to process json from SPADE.
TODO: Let `simple_tracker` to use this package.
"""
import logging
import argparse

VERSION = "v0.0.0.a"
# Register logging
logging.basicConfig(format= '[%(levelname)s]\t%(message)s',level=logging.INFO)


# Register argparser
parser = argparse.ArgumentParser(
    description="A tool to extract cross-namespace operates by id"
)
parser.add_argument(
    "--version",
    "-v",
    action="version",
    version="%(prog)s version : " + VERSION,
    help="show the version",
)
parser.add_argument(
    "--file",
    "-f",
    required=True,
    action="store",
    dest="file",
    help=("JSON file from SPADE to filter"),
    type=argparse.FileType("r"),
)
