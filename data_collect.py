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

    # REFACTOR FOR CHUNKING CASE
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

                    return pd.read_csv(os.listdir()[HandleFile.train_ind], chunksize=chunk_size)
                
                # Just a Normal Dataset
                else:
                    return (pd.read_csv(os.listdir()[HandleFile.train_ind]))
        
        elif os.listdir()[HandleFile.train_ind].endswith('.xlsx'):
            return (pd.read_excel(os.listdir()[HandleFile.train_ind]))
        
    @staticmethod
    def set_test_df():
        if os.listdir()[HandleFile.test_ind].endswith('.csv'):
            
            is_time_series = str(input('Are you dealing with a Time Series Data? Y/N: '))
            chunking = str(input('Do you want to upload the data using chunking? Y/N: '))

            # Normal Data
            if is_time_series.lower() == 'n':
                if chunking.lower() == 'y':
                    chunk_size = int(input('Please Enter the desired chunk size: '))

                    result = []
                    with pd.read_csv(os.listdir()[HandleFile.test_ind], chunksize=chunk_size) as reader:
                        for chunk in reader:
                            result.append(chunk)

                    result = pd.concat(result)
                    result_df = pd.DataFrame(result)

                    return result_df
                
                else:
                    return (pd.read_csv(os.listdir()[HandleFile.test_ind]))
                
            # Time - Series Data
            else:
                ...
            
        elif os.listdir()[HandleFile.test_ind].endswith('.xlsx'):
            return (pd.read_excel(os.listdir()[HandleFile.test_ind]))
