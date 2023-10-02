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

class WrangleNaN:
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
        self.miss_vars()

        # Conditions
        if len(non_miss_var_list_df1) == len(self.df1) and len(non_miss_var_list_df2) == len(self.df2):
            print('Congratulations!!! There are no Missing Values in BOTH the DataFrames')
            print('--'*20)

        else:
            if len(miss_var_list_df1) == 0 and len(miss_var_list_df2) != 0:
                print('The Train dataset DOES NOT contain any variables with Missing Variables')
                print('The Test dataset DOES contain variables with Missing Variables')
                print(f'Number of predictors with Missing Values in Test Dataset:\n {len(miss_var_list_df2)}')
                print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted_df2}')

            elif len(miss_var_list_df1) != 0 and len(miss_var_list_df2) == 0:
                print('The Test dataset DOES NOT contain any variables with Missing Variables')
                print('The Train dataset DOES contain variables with Missing Variables')
                print(f'Number of predictors with Missing Values in Train Dataset:\n {len(miss_var_list_df1)}')
                print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted_df1}')

            else:
                if self.check_miss_var_lists() == 1:
                    print('Both the datasets hold COMMON variables with Missing Values')
                    print(f'Number of common missing values variables: {len(self.check_comm_miss_vars())}')
                    print(f'Variables with Missing Values that are common to both:\n {self.check_comm_miss_vars()}')

                else:
                    print('Both the datasets have different predictors with Missing Values')
                    print(f'Number of predictors with Missing Values in Training Dataset:\n {len(miss_var_list_df1)}')
                    print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted_df1}\n')
                    print(f'Number of predictors with Missing Values in Training Dataset:\n {len(miss_var_list_df2)}')
                    print(f'Variables with Missing Values with their Percentage are:\n {mv_dict_sorted_df2}\n')

        

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

    def miss_vars(self):
        '''
        This function carries out the following tasks:
            1. Determines the predictors with missing values in the given dataframe.
            2. It also calculates the percentage of missing values in each predictor w.r.t. the length of the dataframe.

        Output -> Outputs a list containing the names of the variables with missing values.
        '''
        # For DataFrame 1
        global miss_var_list_df1, non_miss_var_list_df1, mv_dict_sorted_df1
        miss_var_list_df1 = []
        non_miss_var_list_df1 = []
        mv_dict_df1 = dict()
        
        # For DataFrame 1
        for ind, row in enumerate(self.df1.isnull().sum()):
            if row != 0:
                miss_var_list_df1.append(self.df1.columns[ind])
                mv_dict_df1.update({self.df1.columns[ind]: np.round((row / len(self.df1)) * 100, 2)})
            else:
                non_miss_var_list_df1.append(self.df1.columns[ind])

        ## Sorting the predictors on the basis of Missing value proportions
        mv_dict_sorted_df1 = sorted(mv_dict_df1.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        
        # For DataFrame 2
        global miss_var_list_df2, non_miss_var_list_df2, mv_dict_sorted_df2
        miss_var_list_df2 = []
        non_miss_var_list_df2 = []
        mv_dict_df2 = dict()
        
        # For DataFrame 2
        for ind, row in enumerate(self.df2.isnull().sum()):
            if row != 0:
                miss_var_list_df2.append(self.df2.columns[ind])
                mv_dict_df2.update({self.df2.columns[ind]: np.round((row / len(self.df2)) * 100, 2)})
            else:
                non_miss_var_list_df2.append(self.df2.columns[ind])
                
        ## Sorting the predictors on the basis of Missing value proportions
        mv_dict_sorted_df2 = sorted(mv_dict_df2.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    def check_miss_var_lists(self): 
        '''
        Checks whether or not both the datasets contains the same predictors having the missing values.

        Outputs:
            0 : NOT same predictors with Missing variables
            1 : Same predictors with Missing variables
        '''
        if miss_var_list_df1 == miss_var_list_df2:
            return 1
        else:
            return 0
        
    def check_comm_miss_vars(self):
        '''
        Returns a list of Predictors with Missing Values common to both the datasets
        '''
        comm_vars = list(set(miss_var_list_df1).intersection(set(miss_var_list_df2)))
        return comm_vars
    
    def miss_lists(self, df_req):
        '''
        Returns the list of missing variables from the mentioned DataFrames

        # Inputs
            df_req : Integer values that determines the DataFrame
                0 - Only for Training Dataframe
                1 - Only for Test Dataframe
                2 - For both the Dataframes
        '''
        # Assertion
        assert df_req in [0,1,2]

        if df_req == 0:
            return miss_var_list_df1
        
        elif df_req == 1:
            return miss_var_list_df2
        
        else:
            return miss_var_list_df1, miss_var_list_df2



    @staticmethod
    def val_counts(df, pred_list):
        '''
        This function displays value counts for each variable in the pred_list.
        This function is run after the preddictors with missing values are dropped from the dataset.

        Input:
            df : DataFrame
            pred_list : List containing predictors of object dtypes

        * As the function returns a generator object, run the function with list
        '''
        for col in pred_list:
            if col in df.columns:
                yield df[col].value_counts()

    
    @staticmethod
    def rep_obj_vals(df, pred_list, conv_dict):
        """
        This function replaces the object values with given values.

        Input:
            df : DataFrame
            pred_list : List containing predictors of object dtypes (Generally)
            conv_dict : Dictionary used to replace values

        """
        for col in pred_list:
            if col in df.columns:
                yield df[col].replace(conv_dict, inplace=True)

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

        Output format:
            object_dtype, integer_dtype, float_dtype
            The objects are in a list format.
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

class VarExp:

    def var_dump(self, *vars, f_name = 'var_dump.txt'):
        '''
        Dumps the given variables into a .txt file
        '''
        import pickle

        with open(f_name, 'wb') as f:
            pickle.dump(vars, f)
            f.close() 