# Imports
import re
import os
import pandas as pd
from collections import defaultdict as dd

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
        with open(os.listdir()[HandleFile.train_ind]) as tf:
            print(tf)
        with open(os.listdir()[HandleFile.test_ind]) as tsf:
            print(tsf)

    @staticmethod
    def set_train_df():
        if os.listdir()[HandleFile.train_ind].endswith('.csv'):
            is_time_series = str(input('Are you dealing with a Time Series Data? Y/N: '))
            chunking = str(input('Do you want to upload the data using chunking? Y/N: '))
            
            # Dealing with Chunking with Time Series
            if is_time_series.lower() == 'y':

                index_column = str(input('Please Enter the name of the column to be set as index: '))
                date_column = str(input('Please Enter the name of the column containing the dates: '))

                if chunking.lower() == 'n':
                    return (pd.read_csv(os.listdir()[HandleFile.train_ind], index_col=index_column, parse_dates=date_column))
                
                else:
                    chunk_size = int(input('Please Enter the desired chunk size: '))
                    
                    return (pd.read_csv(os.listdir()[HandleFile.train_ind], index_col=index_column, parse_dates=date_column, chunksize=chunk_size))

            # Dealing with Chunking without Time-Series
            else:
                if chunking.lower() == 'y':

                    chunk_size = int(input('Please Enter the desired chunk size: '))

                    return (pd.read_csv(os.listdir()[HandleFile.train_ind], chunksize=chunk_size))
                
                # Just a Normal Dataset
                else:
                    return (pd.read_csv(os.listdir()[HandleFile.train_ind]))
        
        elif os.listdir()[HandleFile.train_ind].endswith('.xlsx'):
            return (pd.read_excel(os.listdir()[HandleFile.train_ind]))
        
    @staticmethod
    def set_test_df():
        if os.listdir()[HandleFile.test_ind].endswith('.csv'):
            return (pd.read_csv(os.listdir()[HandleFile.test_ind]))
        elif os.listdir()[HandleFile.test_ind].endswith('.xlsx'):
            return (pd.read_excel(os.listdir()[HandleFile.test_ind]))
    

class BasicExploration:

    @staticmethod
    def dfShape(train_df, test_df):
        """
        InputsHandleFile
            train_df - Training Dataset
            test_df - Testing Dataset

        Outputs:
            Returns the shapes of the Training and Testing Datasets
        """
        print(f'The shape of the Training dataset is: {train_df.shape}')
        print(f'The shape of the Predicting dataset is: {test_df.shape}')
    
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
    
    @staticmethod
    def dtype_categorize(df):
        '''
        Categorizes the columns on the basis of their dtypes.
        '''
        # Dictionary to hold Columns and their dtypes as key-value pair
        col_dict = dict()

        ## Update the above dictionary
        for x in range(len(df.dtypes)):
            col_dict.update({df.columns[x]:df.dtypes[x]})

        # Grouping on the basis of dtypes
        res = dict()

        for i, v in col_dict.items():
            res[v] = [i] if v not in res.keys() else res[v] + [i]

        # Creating lists on the basis of the keys of res
        lists = dd(list)
        
        for k_name in res.keys():
            lists[k_name].extend(res.get(k_name))
            yield lists[k_name]

            