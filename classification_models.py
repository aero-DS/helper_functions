# Imports
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import ClassifierChain
import numpy as np
## Metrics Imports
from sklearn.metrics import roc_auc_score

class supervBinClass:
    """
    Classification algorithms included in this file are:
        1. Naive Bayes (Linear)
        2. Logistic Regeression (Linear)
        3. K-Nearest Neighbours (Non-parametric)
        4. Support Vector Machines (Linear)
        5. Decision Tree (Tree Based)
        6. Random Forests (Ensemble - Bagging)
        7. Gradient Boosting (Ensemble - Boosting)
    """

    @staticmethod
    def baseline(df1, df2):
        '''
        Gives a baseline score using Logistic Regression for the given performance metric. For a single target, binary classification
        '''
        ... 

class supervMultiLabClass:
    '''
    Supervised MultiLabel-Binary CLassification
    '''
    def __init__(self, train_df, test_baseline = None):

        # Start Time
        st = time.time()

        type_action = input("Are you performing a Baseline Submission Y/N : ")

        # Assertion
        assert type_action.lower() in ['y','n'], 'Only inputs Y and N is valid.'

        self.train_df = train_df
        targ_vars = input('Please Enter the list of Target Variables seperated by a comma: ')
        self.target_vars = list(var for var in targ_vars.split(","))
        
        if type_action.lower() == 'n':
            print(self.pref_metric())

            met = int(input("Please Enter the key for the preferred performance metric to be used: "))
            self.test_split = float(input("Please Enter the test split for the training: "))

            # Baseline Train Model
            true_label, predicted = self.baseline_training(df=self.train_df, target_var=self.target_vars, test_split=self.test_split,     perf_met=met)

            self.Y_test, self.Y_pred = true_label, predicted

            print(eval(self.pref_metric().get(met)))

            # End TIme
            et = time.time()
            print(f'Total Elapsed Time is {round(et-st,2)} seconds')

        else:
            no_ops = int(len(self.target_vars))
            self.test_baseline = test_baseline

            # Baseline Prediction Model
            preds = self.baseline_submission(train_df=self.train_df, target_var=self.target_vars, test_baseline=self.test_baseline)
            
            # Submission File
            base_submission = pd.DataFrame(columns=[var for var in self.target_vars])
            
            ## Assigning the predicted values to the columns
            for idx, col in enumerate(base_submission.columns):
                base_submission[col] = np.array(preds[:,idx])

            # Exporting the Submission File
            base_submission.to_csv('Base_Submisison.csv', index=0)

            # End TIme
            et = time.time()
            print(f'Total Elapsed Time is {round(et-st,2)} seconds')
            

    def pref_metric(self):
        '''
        Dictionary of metrics required for model evaluation techniques for Multi-Label Classification.
        '''
        metric_dict = {
            1: "self.rocaucscore()"
        }
        return metric_dict
    
    # Performance Metrics

    ## ROC_AUC
    
    def rocaucscore(self):
        '''
        roc_auc_score of a multi-label classification model
        '''
        Y_test = self.Y_test
        Y_pred = self.Y_pred
        return round(roc_auc_score(Y_test, Y_pred),3)
    
    # Model

    ## Baseline Training
    def baseline_training(self, df, target_var:list, test_split:float, perf_met:int):
        '''
        Baseline Logistic Regression based estimator for the minimumly pre-processed training dataframe.
        Apart from the required parameter, rest of the parameters are set to be at default state.

        Input:
            df : Train Dataset
            target_var : List of variables considered as the Target variable
            test_split : Split size
            perf_metric : Case-specific Model evaluation criteria
        '''
        # Assertions
        assert type(perf_met) is int, "Input should be an integer from the Performance Dictionary"

        # Variable Assignments
        predictors = [x for x in df.columns if x not in target_var]

        X = df[predictors].values
        Y = df[target_var].values

        # Splitting the Dataframe
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_split)

        # Base Estimator
        base_est = LogisticRegression(multi_class='multinomial')

        # Fit an ensemble of base estimator chains 
        chain = ClassifierChain(base_est, order="random", random_state=0)

        Y_pred = chain.fit(X_train, Y_train).predict(X_test)

        return Y_test, Y_pred
    
    ## Baseline Submission
    def baseline_submission(self, train_df, target_var:list, test_baseline):
        '''
        Baseline submission of the predicted value, to gauge the overall performance of the base model
        '''
         # Variable Assignments
        predictors = [x for x in train_df.columns if x not in target_var]

        X = train_df[predictors].values
        Y = train_df[target_var].values

        # Dealing with the Submission File
        X_test = test_baseline[predictors].values

        # Base Estimator
        base_est = LogisticRegression(multi_class='multinomial')

        # Fit an ensemble of base estimator chains 
        chain = ClassifierChain(base_est, order="random", random_state=0).fit(X,Y)

        # Predictions
        Y_pred = chain.predict(X_test)

        return Y_pred

class supervMultiClsClass:
    '''
    Supervised MultiClass CLassification
    '''
    ...
