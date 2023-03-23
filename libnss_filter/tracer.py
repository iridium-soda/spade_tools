from logger import log
import pandas as pd
class DataModel(object):
# Inlude methods to operate json data and find flow
    def __init__(self,df:pd.DataFrame):
        self.df=df
        # Set index for better query
        self.df = df.set_index(['id'])
    def query_atrifact_id(self,path):
        '''
        To query atrifact in df by its path, return its id
        '''
        return self.df.loc[self.df['annotations.path'] == path][0]['id'] #query result should be the one and only

    def trace_atrifacts_upwards(self,targetid):
        '''
        To trace which artifacts trigger target atrifact with specific id. May cause recursive call.
        '''

    
    
