# Imports
import numpy as np

class DataWrangle:

    def __init__(self, df):
        self.df = df
        self.initial_prep()
        self.miss_var_list()
        self.com_na_var()

    def initial_prep(self):
        '''
        Function carries out an initial check on the given dataframe. The check consists of checking of duplicated rows, and lower cases the
        variable names.
        '''
        # Variable Name Lowering
        self.df.columns = self.df.columns.str.lower()

        # Conditional
        if self.df.duplicated().sum() != 0:
            print('Shape of the dataset before deleting the duplicated rows', self.df.shape)
            print('Number of duplicated rows in the dataset', self.df.duplicated().sum())
            self.df = self.df.drop_duplicates(inplace=True)
            print('Shape of the dataset after deleting the duplicated rows', self.df.shape)
        else:
            print('There are no Duplicated Rows in the dataset!')

        return self.df


    def miss_var_list(self):
        '''
        df: Takes a dataframe as an input. Determines the predictors with missing values and also calculates the percentage of missing values
          in each predictor.

        output: Returns a list containing only the variables with missing values.
        '''
        # Empty lists and dictionary
        miss_var_list = []
        non_miss_var_list = []
        mv_dict = dict()

        # Loop
        for ind, row in enumerate(self.df.isnull().sum()):
            if row != 0:
                miss_var_list.append(self.df.columns[ind])
                mv_dict.update({self.df.columns[ind]: np.round((row / len(df)) * 100, 2)})
            else:
                non_miss_var_list.append(self.df.columns[ind])

        # Printing the List
        if len(non_miss_var_list) == len(self.df):
            print('Congratulations!!! There are no Missing Values in the DataFrame')
        else:
            print(f'Number of Columns with Missing Values:\n {len(miss_var_list)}\n')
            print(f'Variables with Missing Values with their Percentage are:\n {mv_dict}\n')

        return miss_var_list


    def com_na_var(self, df2):
        '''
        Function that checks for presence of common variables with missing variables in both Train and Test
        dataset

        df1: Training Dataset
        df2: Testing Dataset
        '''
         # Conditions
        if len(self.miss_var_list(self.df)) == 0 and len(self.miss_var_list(self.df2)) == 0:
            print('Congratulations!!!, There are no variables with missing values in both the datasets.')

        else:

            if len(self.miss_var_list(self.df)) == 0 and len(self.miss_var_list(self.df2)) != 0:
                print('The first dataset does not contain any variables with Missing Variables')
                print('The second dataset does contain variables with Missing Variables')
                self.miss_var_list(df2)

            elif len(self.miss_var_list(self.df)) != 0 and len(self.miss_var_list(self.df2)) == 0:
                print('The second dataset does not contain any variables with Missing Variables')
                print('The first dataset does contain variables with Missing Variables')
                self.miss_var_list(self.df)

            else:
                if self.miss_var_list(self.df) == self.miss_var_list(self.df2):
                    print('Both the datasets hold common variables with Missing Values')
                elif self.miss_var_list(self.df) != self.miss_var_list(self.df2):
                    print('Both the datasets have different variables with Missing Values')