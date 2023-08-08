# Imports
import numpy as np

class DataWrangle:

    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2
        self.initial_prep()
        self.com_na_var()
        self.obj_dtype_nunique()

    def initial_prep(self):
        '''
        Function carries out an initial check on the given dataframe. The check consists of checking of duplicated rows, and lower cases the
        variable names.
        '''
        # Variable Name Lowering
        self.df1.columns = self.df1.columns.str.lower()
        self.df2.columns = self.df2.columns.str.lower()

        # Conditional
        if self.df1.duplicated().sum() != 0:
            print('Shape of the dataset before deleting the duplicated rows', self.df1.shape)
            print('Number of duplicated rows in the dataset', self.df1.duplicated().sum())
            self.df1 = self.df1.drop_duplicates(inplace=True)
            print('Shape of the dataset after deleting the duplicated rows', self.df1.shape)
        else:
            print('There are no Duplicated Rows in the dataset!')

        return self.df1, self.df2

    @staticmethod
    def miss_var_list(df):
        '''
        df: Takes a dataframe as an input. Determines the predictors with missing values and also calculates the percentage of missing values
          in each predictor.

        output: Returns a list containing only the variables with missing values.
        '''
        # Empty lists and dictionary
        miss_var_list = []
        non_miss_var_list = []

        global mv_dict
        mv_dict = dict()

        # Loop
        for ind, row in enumerate(df.isnull().sum()):
            if row != 0:
                miss_var_list.append(df.columns[ind])
                mv_dict.update({df.columns[ind]: np.round((row / len(df)) * 100, 2)})
            else:
                non_miss_var_list.append(df.columns[ind])

        # Printing the List
        if len(non_miss_var_list) == len(df):
            print('Congratulations!!! There are no Missing Values in the DataFrame')
            print('--'*20)

        return miss_var_list


    def com_na_var(self):
        '''
        Function that checks for presence of common variables with missing variables in both Train and Test
        dataset

        df1: Training Dataset
        df2: Testing Dataset
        '''

        # Global Variables
        global train_df_miss_var_list
        global test_df_miss_var_list

        # Conditions
        if len(DataWrangle.miss_var_list(self.df1)) == 0 and len(DataWrangle.miss_var_list(self.df2)) == 0:
            print('Congratulations!!!, There are no variables with missing values in both the datasets.')

        else:

            if len(DataWrangle.miss_var_list(self.df1)) == 0 and len(DataWrangle.miss_var_list(self.df2)) != 0:
                print('The first dataset does not contain any variables with Missing Variables')
                print('The second dataset DOES contain variables with Missing Variables')

                DataWrangle.miss_var_list(self.df2)
                test_df_miss_var_list = [keys for keys in mv_dict.keys()]
                print(f'Number of predictors with Missing Values in Test Dataset:\n {len(DataWrangle.miss_var_list(self.df2))}')
                print(f'Variables with Missing Values with their Percentage are:\n {mv_dict}')
                return test_df_miss_var_list

            elif len(DataWrangle.miss_var_list(self.df1)) != 0 and len(DataWrangle.miss_var_list(self.df2)) == 0:
                print('The second dataset does not contain any variables with Missing Variables')
                print('The first dataset DOES contain variables with Missing Variables')

                DataWrangle.miss_var_list(self.df1)
                train_df_miss_var_list = [keys for keys in mv_dict.keys()]
                print(f'Number of predictors with Missing Values in Test Dataset:\n {len(DataWrangle.miss_var_list(self.df1))}')
                print(f'Variables with Missing Values with their Percentage are:\n {mv_dict}')
                return train_df_miss_var_list

            else:
                if DataWrangle.miss_var_list(self.df1) == DataWrangle.miss_var_list(self.df2):
                    print('Both the datasets hold COMMON variables with Missing Values')

                    DataWrangle.miss_var_list(self.df1)
                    train_df_miss_var_list = [keys for keys in mv_dict.keys()]
                    return train_df_miss_var_list

                elif DataWrangle.miss_var_list(self.df1) != DataWrangle.miss_var_list(self.df2):
                    print('Both the datasets have different predictors with Missing Values')

                    print(f'Number of predictors with Missing Values in Training Dataset:\n {len(DataWrangle.miss_var_list(self.df1))}')
                    DataWrangle.miss_var_list(self.df1)
                    train_df_miss_var_list = [keys for keys in mv_dict.keys()]
                    print(f'Variables with Missing Values with their Percentage are:\n {mv_dict}\n')

                    print(f'Number of predictors with Missing Values in Test Dataset:\n {len(DataWrangle.miss_var_list(self.df2))}')
                    DataWrangle.miss_var_list(self.df2)
                    test_df_miss_var_list = [keys for keys in mv_dict.keys()]
                    print(f'Variables with Missing Values with their Percentage are:\n {mv_dict}\n')
                    return train_df_miss_var_list, test_df_miss_var_list
                
    def obj_dtype_nunique(self):
        '''
        Returns nuumber of unique values for all the predictors with "object" dtype
        '''
        print('--'*20)
        print('List of Predictors of Object dtypes with the number of unique values')
        print('--'*20)
        for col in self.df1.columns:
            if self.df1.dtype == 'object':
                print(f'{col}:{self.df1[col].nunique()}')