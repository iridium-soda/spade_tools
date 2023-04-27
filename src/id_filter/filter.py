"""
"""
from utils import *
from utils.utils import *
import logging


def do_filter(raw_json: list[dict]) -> None:
    # Find objects inside the container
    processes = list()  # All nodes whose type are 'Process'
    edges = list()  # All edges which contain 'from' and 'to'
    for obj in raw_json:
        if obj["type"] == "Process":
            processes.append(obj)
            if (
                obj["annotations"]["gid"] != "0"
                and obj["annotations"]["euid"] != "0"
                and obj["annotations"]["uid"] != "0"
                and obj["annotations"]["egid"] != "0"
            ):
                logging.info("Internal artifact captured\n"+better_display_json(obj))
