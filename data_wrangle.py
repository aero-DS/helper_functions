# Imports
from typing import Any
import matplotlib.pyplot  as plt
import numpy as np

class BasicExploration:

    '''
    This class performs the following tasks:
        1. Returns the shape of the Train and Test Datasets.
        2. Checks for the expected discrepancies.
        3. Checks for presence of Missing values in the Train and Test Dataset.
        4. Lowercases the predictor names.
    '''

    def __init__(self, train_df, test_df):
        self.df1 = train_df
        self.df2 = test_df
        

    def __call__(self):
        self.dfShape()
        if len(self.col_discrp()) == 1:
            self.stnd_col_names()
            print('---'*20)
            print('Column Discrepancy as expected.')
            self.check_dupl()
            print('---'*20)
            print('Unique Column Data Types:\n', list(self.df1.dtypes.unique()))
            print('---'*20)

            if self.check_na() == 0:
                print('There is no presence of Missing Value in the Dataframe.')
                print('---'*20)
            else:
                print(f'There is presence of {self.check_na()} predictors with missing values.')
                print('---'*20)
        
        else:
            print('Unexpected Column Discrepancy!!')

    def dfShape(self):
        """
        InputsHandleFile
            train_df - Training Dataset
            test_df - Testing Dataset

        Outputs:
            Returns the shapes of the Training and Testing Datasets
        """
        print('Shape of the Training Dataset')
        print(f'Number of Rows: {self.df1.shape[0]}')
        print(f'Number of Columns: {self.df1.shape[1]}')

        print('---'*20)

        print('Shape of the Testing Dataset')
        print(f'Number of Rows: {self.df2.shape[0]}')
        print(f'Number of Columns: {self.df2.shape[1]}')

    def col_discrp(self):
        """
        This function checks the presence of predictors that are NOT present in both datasets.

        Output: Returns a list of non-common predictors.

        * Dataset Validation of sorts
        """
        return list(set(self.df1.columns).symmetric_difference(set(self.df2.columns)))
    
    def check_dupl(self):
        """
        Checks the presence of duplicated rows in the Train Dataset
        """
        global dupl_val
        dupl_val = self.df1.duplicated().sum()

        if dupl_val != 0:
            print('There is  presence of duplicated rows in the dataset')
        
        else:
            print('Dataset is free of Duplicated rows.')

    def check_na(self):
        """
        Checks for the presence of Missing Values in the Dataframe
        """
        global na_val
        na_val = len(self.df1.columns[self.df1.isnull().any()].tolist())
        return na_val
    
    def stnd_col_names(self):
        """
        Converts the col names into the lower case
        """
        self.df1.columns = self.df1.columns.str.lower()
        self.df2.columns = self.df2.columns.str.lower()

class DataFlt(BasicExploration):
    """
    Filters the dataframe from the irregularities.
    
    Performs the following operations:
        1. If exists, removes duplicated rows, identifies predictors with missing values.
        2. If needed, standardizes the col-names for proper readibility.
        3. Checks for Outliers in the numeric predictors.
        4. Checks for  Class Imbalance for categorical predictors.

    Inputs:
        typ_analysis:
            1 - Regression Analysis
            2 - Classification Analysis
    """

    def __init__(self,train_df, test_df,typ_analysis, targ_var):
        self.df1 = train_df
        self.df2 = test_df
        self.typ_analysis = typ_analysis
        self.targ_var = targ_var
        
    def __call__(self):
        # Dealing with Duplicated and Missing Rows
        if dupl_val != 0 and na_val != 0:
            self.rem_dupl_var()
            print('Shape of the dataset after deleting the duplicated rows', self.df1.shape)
            self.miss_vars()
            if self.check_miss_var_lists() == 1:
                print('Both the Datasets have the SAME predictors with missing values.')
                print(f'Common Missing Value Predictors are:\n {self.check_comm_miss_vars()}')
            else:
                print('Both the Datasets have the DIFFERENT predictors with missing values.')
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

        elif dupl_val != 0 and na_val == 0:
            self.rem_dupl_var()
            print('Shape of the dataset after deleting the duplicated rows', self.df1.shape)

        elif dupl_val == 0 and na_val != 0:
            self.miss_vars()
            if self.check_miss_var_lists() == 1:
                print('Both the Datasets have the SAME predictors with missing values.')
                print(f'Common Missing Value Predictors are:\n {self.check_comm_miss_vars()}')
            else:
                print('Both the Datasets have the DIFFERENT predictors with missing values.')
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
            print("Training Dataset is free of Duplicate Rows and Missing Values.")

        # Problem-based Target Variable Analysis
        if self.typ_analysis == 2:
            majority_Variable,maj_value ,minority_variable, min_value = self.det_class_imbl()
            print(f'Value with the Majority Proportion in the Target Variable- {majority_Variable} : {maj_value}')
            print(f'Value with the Minority Proportion in the Target Variable- {minority_variable} : {min_value}')

        else:
            ...

    def rem_dupl_var(self):
        """
        Removes the duplicated rows from the Training Dataset.
        """
        self.df1 = self.df1.drop_duplicates(inplace=True)
        
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
    
    def miss_var_prop(self):
        '''
        Returns the proportion of missing value predictors for a Training Dataset.

        Output is a sorted form sorted form of the missing value proportion dictionary.
        '''
        return dict(mv_dict_sorted_df1)
    
    def miss_lists(self, df_req):
        '''
        Returns the list of missing variables from the mentioned DataFrames

        # Inputs
            df_req : Integer values that determines the DataFrame
                0 - Only for Training Dataframe - Preferred for COMMON missing variables
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
        
    def miss_var_thresholding(self, miss_var_prop_dict, thr_val:int):
        '''
        Drops the columns with missing variable proportions greater than the threshold value
        '''
        thr_miss_vars = []

        for key in miss_var_prop_dict.keys():
            if miss_var_prop_dict[key] <= thr_val:
                thr_miss_vars.append(key)

        return thr_miss_vars
    
    def dtype_categorize(self):
        '''
        Categorizes the columns on the basis of their dtypes.

        Output format:
            ob_dtype, int_dtype, dt_dtype, flt_dtype
            The objects are in a list format.
        '''
        req_cols = self.df1.columns.tolist()
        req_cols.remove(self.targ_var)

        # Dictionary to hold Columns and their dtypes as key-value pair
        col_dict = dict()

        ## Update the above dictionary
        for x in range(len(self.df1[req_cols].dtypes)):
            col_dict.update({self.df1[req_cols].columns[x]:self.df1[req_cols].dtypes[x]})

        # Grouping on the basis of dtypes
        res = dict()

        for i, v in col_dict.items():
            res[v] = [i] if v not in res.keys() else res[v] + [i]

        # Imports
        from collections import defaultdict as dd

        # Creating lists on the basis of the keys of res
        lists = dd(list)
        
        for k_name in res.keys():
            lists[k_name].extend(res.get(k_name))
            yield lists[k_name]

    def uniq_vals_num(self, thr:int=10):
        """
        1. Determines number of unique values in a predictors.
        2. Depending on the threshold value, returns a list containing names of predictors which can be converted into 'Category' dtype.

        Inputs:
            thr: Number of nunique values required for the pred to be categorized as an ideal canidate
        """
        # Number of Unique Values Dictionary
        num_unq = dict(self.df1.nunique())

        # Comparing the unique values with the Threshold Value
        thr_preds = list(filter(lambda x: num_unq[x] < thr,num_unq))

        return thr_preds
    
    def re_organize_dlists(self, *org_dlists, cat_dtyp):
        """
        Removes the misinterpreted variables from the given 
        """
        for dlist in org_dlists:
            com_var = list(set(dlist).intersection(set(cat_dtyp)))
            if len(com_var) != 0:
                for ele in com_var:
                    dlist.remove(ele)
                yield dlist
            else:
                yield dlist

    @staticmethod
    def det_outliers_iqr(df,col):
        """
        Retruns the length of outliers in a predictor.
        """
        outl = []
        srt_data = sorted(df[col])

        # IQR Calculations
        import numpy as np
        q1 = np.percentile(srt_data, 25)
        q3 = np.percentile(srt_data, 75)
        IQR = q3-q1
        lwr_bound = q1-(1.5*IQR)
        upr_bound = q3+(1.5*IQR)

        for i in srt_data: 
            if (i<lwr_bound or i>upr_bound):
                outl.append(i)

        return len(outl)
    
    @staticmethod
    def preds_w_outl(df,cols):
        """
        Returns the list of names of predictors with outliers.
        """
        outl_preds = []

        for col in cols:
            if DataFlt.det_outliers_iqr(df, col) != 0:
                outl_preds.append(col)

        return outl_preds
    
    def det_class_imbl(self):
        """
        Checks the column for class imbalance and Classifying the majority and minority classes in the Target Variable.
        """
        global val_cnt_dict
        val_cnt_dict = dict()
        for val in self.df1[self.targ_var].unique():
            val_cnt = len(self.df1[self.df1[self.targ_var]==val])
            val_cnt_prop = round(val_cnt / len(self.df1[self.targ_var]), 2)
            val_cnt_dict.update({val:val_cnt_prop})

        # Classifying the Value Classes

        ## Determine the Major Class
        global maj_val
        maj_val = 0
        maj_ky = ''
        for val_ky in val_cnt_dict.keys():
            if val_cnt_dict[val_ky] > maj_val:
                maj_val = val_cnt_dict[val_ky]
                maj_ky = val_ky

        ## Determine the Minor Class
        global min_val
        min_val = maj_val
        min_ky = ''

        for val_ky in val_cnt_dict.keys():
            if val_cnt_dict[val_ky] < min_val:
                min_val = val_cnt_dict[val_ky]
                min_ky = val_ky

        return maj_ky,maj_val, min_ky,min_val 

class TypeCasting(DataFlt):

    def __init__(self, chg2int_list=None, chg2int_list_ky=None, chg2flt_list=None, chg2flt_list_ky=None, chg2cat_list=None, chg2cat_list_ky=None):
        
        # Predictors to be Changed List
        self.chg2int_list = chg2int_list
        self.chg2flt_list = chg2flt_list
        self.chg2cat_list = chg2cat_list

        # Change List format
        self.chg2int_list_ky = chg2int_list_ky
        self.chg2flt_list_ky = chg2flt_list_ky
        self.chg2cat_list_ky = chg2cat_list_ky

    def __call__(self, tr_df = None, te_df = None):
        
        self.df1 = tr_df
        self.df2 = te_df

        if self.df1:
            
            if self.chg2int_list:
                self.chg2int(df=self.df1)
            else:
                pass

            if self.chg2int_list:
                self.chg2int(df=self.df1)
            else:
                pass

            if self.chg2int_list:
                self.chg2int(df=self.df1)
            else:
                pass

            if self.chg2cat_list:
                self.chg2cat(df=self.df1)
            else:
                pass

        else:
            pass

        if self.df2:
            
            if self.chg2int_list:
                self.chg2int(df=self.df2)
            else:
                pass

            if self.chg2int_list:
                self.chg2int(df=self.df2)
            else:
                pass

            if self.chg2int_list:
                self.chg2int(df=self.df2)
            else:
                pass

            if self.chg2cat_list:
                self.chg2cat(df=self.df2)
            else:
                pass

        else:
            pass
    
    def chg2int(self,df):
        """
        For a list of predictors, this function changes the dtype to "int". Variation needs to be provided.
        """
        return df[self.chg2int_list].astype(self.chg2int_list_ky)
    
    def chg2flt(self,df):
        """
        For a list of predictors, this function changes the dtype to "float". Variation needs to be provided.
        """
        return df[self.chg2flt_list].astype(self.chg2flt_list_ky)
    
    def chg2cat(self,df):
        """
        For a list of predictors, this function changes the dtype to "Category". Variation needs to be provided.
        """
        return df[self.chg2cat_list].astype(self.chg2cat_list_ky)

class DataVisualize(TypeCasting):
    '''
    Data Visualization for Target Variables and Predictor Columns.
    
    Legend:
        1 - Continuous Target Variable
        2 - Classification Target Variable
    '''

    def __init__(self, df, targ_var, targ_var_typ:int):
        self.df1 = df
        self.targ_var = targ_var
        if targ_var_typ == 1:
            self.vis_tar_var()
        else:
            print('Please Enter the Type of Target Variables')

    def num_preds_viz(self, num_preds):
        """
        Creates a Histogram for the predictors with integer dtypes.
        """
        import matplotlib.pyplot as plt
        import numpy as np

        fig = plt.figure(figsize = (75,35))
        n_rows = int(np.ceil(len(num_preds)/3))

        for ind,pred in enumerate(num_preds):
            fig = plt.figure(figsize = (15,7))
            plt.subplot(n_rows,3,ind+1)
            self.df1[pred].hist()
            plt.title(pred)
            plt.show()

    def vis_tar_var(self):
        '''
        Outputs a line graph and a box-plot side-by-side for a numeric target variable

        col : Name of the Target Variable
        '''
        y_label_name = input('Please Enter the name of the desired y_label: ')
        fig = plt.figure(figsize = (15,7))
        # For Box-Plot
        plt.subplot(1, 2, 1)
        plt.boxplot(self.df[self.targ_var])
        plt.ylabel(y_label_name)
        # For Line Graph
        plt.subplot(1, 2, 2)
        plt.plot(self.df[self.targ_var])
        plt.ylabel(y_label_name)
        plt.show()

    
class VarExp:
    '''
    This class performs the following tasks:
        1. Makes a new directory.
        2. Exports the variable associated with train dataframe
        3. Dumps the variables for future uses
    '''
    
    def __init__(self, dir_path_name:str):
        self.dir_path_name = dir_path_name
        self.create_dir()
        
    def create_dir(self):
        '''
        Creates a new directory with the given name
        '''
        # Import
        import os

        if os.path.exists(os.path.join(os.path.join(os.getcwd(), self.dir_path_name))):
            print('Directory with the same name already exists.')
            rem_cnf = str(input('Do you want to choose a another name for the directory? (y/n): '))

            assert rem_cnf.lower() in ['y','n'], 'Select properly.'

            if rem_cnf.lower() == 'n':
                os.rmdir()
                return os.mkdir(self.dir_path_name)
            else:
                new_dir_name = str(input('Please enter a new name for the directory: '))
                self.dir_path_name = new_dir_name
                return os.mkdir(self.dir_path_name)
    
    def var_dump(self, *vars, f_name = 'var_dump.pkl'):
        '''
        Exports the variables onto a pickle file
        '''
        # Imports
        import os
        import pickle
        
        path_dir = os.path.join(self.dir_path_name, f_name)
        with open(path_dir, 'wb') as f:
            pickle.dump(vars, f)
            f.close()