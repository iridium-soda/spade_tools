import logging
def get_logger(name='root'):
    logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)
    return logging.getLogger(name)
 
 
log = get_logger(__name__)
