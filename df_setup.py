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

                    result = []
                    with pd.read_csv(os.listdir()[HandleFile.train_ind], chunksize=chunk_size) as reader:
                        for chunk in reader:
                            result.append(chunk)

                    result = pd.concat(result)
                    result_df = pd.DataFrame(result)

                    return result_df
                
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


class BasicExploration:

    '''
    This class performs the following tasks:
        1. Returns the shape of the Train and Test Datasets.
        2. Checks for the expected discrepancies.
        3. Removes the duplicated rows and lowers the names of the predictors in both the datasets.
    '''

    def __init__(self, train_df, test_df):
        self.df1 = train_df
        self.df2 = test_df
        self.dfShape()
        if len(self.col_discrp()) == 1:
            print('Discrepancy as expected')
            self.rem_dup_lw_var()
        else:
            print('Unexpected Discrepancy. ')

    def dfShape(self):
        """
        InputsHandleFile
            train_df - Training Dataset
            test_df - Testing Dataset

        Outputs:
            Returns the shapes of the Training and Testing Datasets
        """
        print(f'The shape of the Training dataset is: {self.df1.shape}')
        print(f'The shape of the Predicting dataset is: {self.df2.shape}')

    def col_discrp(self):
        """
        This function checks the presence of predictors that are NOT present in both datasets.

        Output: Returns a list of non-common predictors.

        * Dataset Validation of sorts
        """
        return list(set.symmetric_difference(set(self.df1.columns), set(self.df2.columns)))

    def rem_dup_lw_var(self):
        '''
        This function carries out 2 tasks:
            1. Lowers the variable names of the dataframes.
            2. Removes the duplicated rows from the training dataset.
        '''
        # Variable Name Lowering
        self.df1.columns = self.df1.columns.str.lower()
        self.df2.columns = self.df2.columns.str.lower()

        # To deal with duplicated rows
        if self.df1.duplicated().sum() != 0:
            print('Shape of the dataset before deleting the duplicated rows', self.df1.shape)
            print('Number of duplicated rows in the dataset', self.df1.duplicated().sum())
            self.df1 = self.df1.drop_duplicates(inplace=True)
            print('Shape of the dataset after deleting the duplicated rows', self.df1.shape)
        else:
            print('There are no Duplicated Rows in the dataset!')

    @staticmethod
    def dtype_categorize(df):
        '''
        Categorizes the columns on the basis of their dtypes.

        Output format:
            ob_dtype, int_dtype, dt_dtype, flt_dtype
            The objects are in a list format.
        '''
        # Imports
        from collections import defaultdict as dd

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