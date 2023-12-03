class Baselinedf_Reg:

    """
    This class performs the following taks:
        1. Readies the Dataframe for the Baseline Model Performance.
    """

    def __init__(self, df, cols2drp):
        self.df = df
        self.cols2drp = cols2drp

    def __call__(self):

        if self.cols2drp != None:
           self.df.drop(columns=self.cols2drp, axis=1, inplace=True)
        else:
            pass

    def miss_vars(self):
        miss_vars = [col for col in self.df.columns if self.df[col].isna().sum()>0]
        return miss_vars
    
    def splt_and_exp_str(self, col, splt_crt):
        """
        Splits a string and then expands it into new columns.
        """
        return self.df[col].str.split(splt_crt, expand=True)
    
    # THROWS VALUEERROR - WORKS IN LOOP
    @staticmethod
    def det_nanmap_multistr(*sup_cols,tmp_df,base_col):
        """
        This function uses the newly created columns by column split in the previous function, to help in mapping the values
        for predictors with missing values.

        Inputs:
            *sup_cols : List of predictors that would be used for values determination
            tmp_df : Sub-Dataframe without any NaN
            base_col : Predictor to be used for purposes of grouping

        Output:
            Is in the form of a Dictionary.

        Constraints:
            1. The order of the list contents for the sup_cols will determine the value output format.
            2. The tmp_df needs to be created before and needs to be without missing value predictors.
            3. Dealing with Date Cases only.

        """
        # Library
        import pandas as pd

        # Determining the Max values for each Index keys
        main_map = dict()
        for sup_col in sup_cols: 
            sup_crosstab = pd.crosstab(index=tmp_df[base_col], columns=tmp_df[sup_col])

            for ky in sup_crosstab.index:
                map_val = sup_crosstab.loc[ky].idxmax()
                
                if ky not in main_map.keys():
                    main_map.update({ky:[map_val]})
                else:
                    main_map[ky]+=[map_val]

        # Joining the values of the main_map as per the given format
        join_req = int(input("Do you want the join the values of values? 0/1 : "))

        if join_req == 1:
            join_frmt = input("Please enter the Join format for the values : ")
            fin_dict = dict()

            for ky,vals in main_map.items():
                fin_dict.update({ky:join_frmt.join(vals)})
        else:
            return main_map
        
        return fin_dict