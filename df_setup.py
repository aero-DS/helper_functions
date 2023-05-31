# Imports
import re
import os
import pandas as pd

# Parent Class
from initial import *

class DfSetup(HandleFile):
    
    """
    Class handles the following processes:
        1. Provides the encoding information about the data files.
        2. Creates test and train dataframes.
        3. Provides the shape information and overview of the dataframes.
    """
    
    def __init__(self) :
       self.encod_config()

    def encod_config(self):
        with open(os.listdir()[super.data_ind()[0]]) as tf:
            print(tf)
        with open(os.listdir()[super.data_ind()[1]]) as tsf:
            print(tsf)

    @staticmethod
    def set_train_df():
        if os.listdir()[HandleFile.data_ind()[0]] == 'csv':
            return (pd.read_csv(os.listdir()[HandleFile.data_ind()[0]]))
        else:
            return (pd.read_excel(os.listdir()[HandleFile.data_ind()[0]]))
        
    @staticmethod
    def set_test_df():
        if os.listdir()[HandleFile.data_ind()[1]] == 'csv':
            return (pd.read_csv(os.listdir()[HandleFile.data_ind()[1]]))
        else:
            return(pd.read_excel(os.listdir()[HandleFile.data_ind()[1]]))
    

class BasicExploration:

    @staticmethod
    def dfShape(train_df, test_df):
        """
        InputsHandleFile
            train_df - Training Dataset
            test_df - Testing Dataset

        Outputs:
            Returns the shaoes of the Training and Testing Datasets
        """
        print(f'The shape of the Training dataset is {train_df.shape}')
        print(f'The shape of the Predicting dataset is {test_df.shape}')

    @staticmethod
    def overview(df):
        return df.info(), df.describe()
    
    @staticmethod
    def split_str(df, splt_crt:str, str_ind_int:int, len_req:str=False, maxsplit=-1):
        """
        Splitting the strings in a given Dataframe Column with an optional length of those strings.

        Inputs:
            df - DataFrame Column
            splt_crt - Splitting Criteria
            splt_ind_int - The index of the splitted string that needs to be used
            len_req - Length
        """
        if len_req==False:
            split_string =  df.map(lambda x: x.split(splt_crt, maxsplit)[str_ind_int])
            return split_string
        else:
            split_string_len =  df.map(lambda x: x.split(splt_crt, maxsplit)[str_ind_int]).map(lambda x: len(x))
            return split_string_len
        
    
    @staticmethod
    def multiStringReplace(oldString, oldValueList, newValue):
        '''
        Replacing multiple strings to a single new string.
        '''
        for oldValue in oldValueList:
            oldString = oldString.replace(oldValue, newValue)

        return oldString
    
    