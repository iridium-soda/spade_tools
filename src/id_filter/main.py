import json
import filter
from utils import *
VERSION = "v0.0.0.a"
if __name__ == "__main__":
    
    args = parser.parse_args()
    file_handle = args.file
    # Print info
    logging.info("File got:%s" % file_handle.name)

    # Load data from file
    recs = json.load(file_handle)  # Usually recs should be list[dict]
    logging.info("json dumped")
    logging.debug("Raw json is:\n", json.dumps(recs, indent=2, separators=(",", ": ")))

    # Close the file handle
    file_handle.close()

    # TODO:把simple_tarcker改组一下，把能用的API抽出来弄个utils
