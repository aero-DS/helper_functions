# Imports
import matplotlib as plt
import numpy as np

class DataVisualize:
    '''
    This class carries-out the following tasks:
        1. Visualize the Numeric Target Variable.
    '''
    
    @staticmethod
    def vis_tar_var(col):
        '''
        Outputs a line graph and a box-plot side-by-side for a numeric target variable

        col : Name of the Target Variable
        '''
        y_label_name = input('Please Enter the name of the desired y_label: ')
        fig = plt.figure(figsize = (15,7))
        # For Box-Plot
        plt.subplot(1, 2, 1)
        plt.boxplot(col)
        plt.ylabel(y_label_name)
        # For Line Graph
        plt.subplot(1, 2, 2)
        plt.plot(col)
        plt.ylabel(y_label_name)
        plt.show()

class DataWrangle:
    '''
    Class handles the following processes:
        1. Removes duplicated rows from the training data.
        2. Lowers the variable names of both the datasets.
        3. Return a list containing only the variables with missing values.
        4. Return a dictionary with the name of the variable and the percentage of missing value in it.
    '''

    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2
        self.rem_dup_lw_var()
        self.comm_nan_vars()

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
    def miss_var_list(df):
        '''
        This function carries out the following tasks:
            1. Determines the predictors with missing values in the given dataframe.
            2. It also calculates the percentage of missing values in each predictor w.r.t. the length of the dataframe.
        
        df -> Input Dataframe

        Output -> Outputs a list containing the names of the variables with missing values.
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

        global mv_dict_sorted
        mv_dict_sorted = sorted(mv_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

        # Printing the List
        if len(non_miss_var_list) == len(df):
            print('Congratulations!!! There are no Missing Values in the DataFrame')
            print('--'*20)

        else:
            return miss_var_list
        

    def comm_nan_vars(self):
        '''
        This function carries out the following tasks:
            1. Checks for presence of common variables with missing values in train and test dataframe.
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
                print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted}')

                return test_df_miss_var_list
            
            elif len(DataWrangle.miss_var_list(self.df1)) != 0 and len(DataWrangle.miss_var_list(self.df2)) == 0:
                print('The second dataset does not contain any variables with Missing Variables')
                print('The first dataset DOES contain variables with Missing Variables')

                DataWrangle.miss_var_list(self.df1)
                train_df_miss_var_list = [keys for keys in mv_dict.keys()]
                
                print(f'Number of predictors with Missing Values in Test Dataset:\n {len(DataWrangle.miss_var_list(self.df1))}')
                print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted}')

                return train_df_miss_var_list
            
            else:
                if DataWrangle.miss_var_list(self.df1) == DataWrangle.miss_var_list(self.df2):
                    print('Both the datasets hold COMMON variables with Missing Values')

                    DataWrangle.miss_var_list(self.df1)
                    train_df_miss_var_list = [keys for keys in mv_dict.keys()]
                    
                    # Need to sort out the sorted equivalent for this case

                    return train_df_miss_var_list

                elif DataWrangle.miss_var_list(self.df1) != DataWrangle.miss_var_list(self.df2):
                    print('Both the datasets have different predictors with Missing Values')

                    print(f'Number of predictors with Missing Values in Training Dataset:\n {len(DataWrangle.miss_var_list(self.df1))}')
                    DataWrangle.miss_var_list(self.df1)
                    train_df_miss_var_list = [keys for keys in mv_dict.keys()]
                    
                    print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted}\n')

                    print(f'Number of predictors with Missing Values in Test Dataset:\n {len(DataWrangle.miss_var_list(self.df2))}')
                    DataWrangle.miss_var_list(self.df2)
                    test_df_miss_var_list = [keys for keys in mv_dict.keys()]
                    
                    print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted}\n')

                    com_vars = set(train_df_miss_var_list).intersection(set(test_df_miss_var_list))
                    print(f'Number of common missing values variables: {len(com_vars)}')
                    print(f'Variables with Missing Values that are common to both:\n {com_vars}')

                    return train_df_miss_var_list, test_df_miss_var_list