import argparse
import logging
import json
VERSION="v0.0.0.a"
if __name__=="__main__":

    # Register argparser
    parser = argparse.ArgumentParser(description="A tool to extract cross-namespace operates by id")
    parser.add_argument('--version', '-v', action='version',
                    version='%(prog)s version : '+VERSION, help='show the version')
    parser.add_argument('--file', '-f', required=True,action='store',
                    dest='file',
                    help=('JSON file from SPADE to filter'),
                    type=argparse.FileType('r'))
    args=parser.parse_args()
    file_handle=args.file

    # Register logger
    logging.basicConfig(level=logging.DEBUG,format= '[%(levelname)s]\t%(message)s')
    
    # Print info
    logging.info("File got:%s"%file_handle.name)

    # Load data from file
    json.load(file_handle)
    logging.info("json dumped")

    # TODO:把simple_tarcker改组一下，把能用的API抽出来弄个utils，上cmd-utils架构

    


