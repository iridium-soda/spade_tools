
import pandas as pd
import sys
import json
import os
from logger import log
import tracer
def main(path:str)->None:
    try:
        with open(path, 'r') as f:
            rawjsons = f.read()
            df = json.loads(rawjsons)    
        
    except IOError:
        log.exception("Unable to open or read %s",path)
    df = pd.json_normalize(df)
    model=tracer.DataModel(df=df)# All operations are executed in this class


if __name__=="__main__":
    usage="python3 libnss_extractor.py <SPADE_raw_json>"
    log.basicConfig(format='%(levelname)s:%(message)s',level=log.DEBUG)
    try:
        if len(sys.argv) != 2:
            log.exception(usage)
        else:
            jsonpath=sys.argv[1]
            print("Starting...")
            log.info("Input json is %s"%jsonpath)
            main(jsonpath)
    except KeyboardInterrupt:
        print("Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)