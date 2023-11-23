class Feat_eng:
    '''
    Performs the following tasks related to Feature Engineering:
    '''

    def __init__(self, df1):
        self.df1 = df1

    def multival_pred_cnt(self, pred_lst, splt_crt):
        '''
        For a predictor with multiple object values for a single record, returns the frequency of occurrences.

        Inputs:
            pred_lst: List of predictors
            splt_crt: Criteria for Splitting the values

        Output needs to be formatted into a list.
        '''
        for pred in pred_lst:
            spl = []
            for i in range(len(self.df1)):
                try:
                    splt_row = self.df1[pred][i].split(splt_crt)
                    for sub_lst in splt_row:
                        spl.append(sub_lst)

                except:
                    continue

            col_spl_dct = dict()
            for val in spl:
                if val not in col_spl_dct.keys():
                    col_spl_dct.update({val:1})
                else:
                    col_spl_dct.update({val:col_spl_dct[val]+1})

            yield col_spl_dct