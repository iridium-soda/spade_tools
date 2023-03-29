import pandas as pd
import sys
import json
import os
from logger import log
import tracer

TARGET_PATH="/lib/x86_64-linux-gnu/libnss_files.so.2"

def main(path: str,maxlev:int) -> None:
    global TARGET_PATH
    try:
        with open(path, "r") as f:
            rawjsons = f.read()
            df = json.loads(rawjsons)

    except IOError:
        log.exception("Unable to open or read %s", path)
    df = pd.json_normalize(df)
    model = tracer.DataModel(df=df)  # All operations are executed in this class
    # print(model.df)
    ids=model.trace_atrifacts_upwards_by_path(TARGET_PATH,maxlev)
    log.info("The following path are extracted in %d level:\n%s",maxlev,ids)


if __name__ == "__main__":
    usage = "python3 libnss_extractor.py <SPADE_raw_json> <maxium_level>"
    try:
        if len(sys.argv) != 3:
            log.exception(usage)
        else:
            jsonpath = sys.argv[1]
            maxlev=sys.argv[2]
            print("Starting...")
            log.info("Input json is %s" % jsonpath)
            main(jsonpath,maxlev)
    except KeyboardInterrupt:
        print("Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
