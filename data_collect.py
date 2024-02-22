import os
from initial import HandleFile
import pandas as pd


class DfSetup:
    """
    This class performs the following tasks:
        1. Provides the encoding information about the files.
        2. Creates Train and Test dataframe.
    """

    def encod_config(self):
        "Provides encoding information about the files to be uploaded for the dataframes."

        if HandleFile.search_type == 0:
            with open(os.listdir()[HandleFile.train_ind]) as tf:
                print(tf)
            with open(os.listdir()[HandleFile.test_ind]) as tsf:
                print(tsf)

        else:
            with open(HandleFile.get_train_file_path()) as tf:
                print(tf)
            with open(HandleFile.get_test_file_path()) as tsf:
                print(tsf)

    def set_train_df(self):
        """
        This function loads the train data file as a pandas dataframe.
        """
        if HandleFile.get_search_type() == 0:
            if os.listdir()[HandleFile.get_train_ind()].endswith('.csv'): 
                return pd.read_csv(os.listdir()[HandleFile.get_train_ind()])
            else:
                return pd.read_excel(os.listdir()[HandleFile.get_train_ind()])
        
        else:
            if HandleFile.get_train_file_path().endswith('.csv'):
                return pd.read_csv(HandleFile.get_train_file_path())
            else:
                return pd.read_excel(HandleFile.get_train_file_path())

            
    def set_test_df(self):
        """
        This function loads the train data file as a pandas dataframe.
        """
        if HandleFile.get_search_type() == 0:
                if os.listdir()[HandleFile.get_test_ind()].endswith('.csv'): 
                    return pd.read_csv(os.listdir()[HandleFile.get_test_ind()])
                else:
                    return pd.read_excel(os.listdir()[HandleFile.get_test_ind()])
            
        else:
            if HandleFile.get_test_file_path().endswith('.csv'):
                return pd.read_csv(HandleFile.get_test_file_path())
            else:
                return pd.read_excel(HandleFile.get_test_file_path())