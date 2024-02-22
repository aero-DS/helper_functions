# Imports
import os
import re

class HandleFile:
    """
    Class handles the following tasks:
        1. Provides the indices of the train, test and submission data file to the child class.
        2. Also provides the indices for other csv files pertaining to the train datasets.
    """

    # Initial State

    ## Index Based Search
    train_ind:int = None
    test_ind:int = None
    sampl_sub_ind:int = None
    class_samp_file_state:int = None

    ## Name Based Search
    train_file_path:str = None
    test_file_path:str = None

    ## Search Type (0: Index based, 1: Name based)
    search_type:int = None

    # Class Variable Methods
    ## 1
    @classmethod
    def get_train_ind(cls):
        return cls.train_ind
    
    ## 2
    @classmethod
    def set_train_ind(cls, value:int):
        cls.train_ind = value

    ## 3
    @classmethod
    def reset_train_ind(cls):
        cls.train_ind = None

    ## 4
    @classmethod
    def get_test_ind(cls):
        return cls.test_ind
    
    ## 5
    @classmethod
    def set_test_ind(cls, value:int):
        cls.test_ind = value

    ## 6
    @classmethod
    def reset_test_ind(cls):
        cls.test_ind = None

    ## 7
    @classmethod
    def get_sampl_file_pres_state(cls):
        return cls.class_samp_file_state
    
    ## 8
    @classmethod
    def set_sampl_file_pres_state(cls,value:str):
        cls.class_samp_file_state = value

    ## 9
    @classmethod
    def reset_sampl_file_pres_state(cls):
        cls.class_samp_file_state = None

    ## 10
    @classmethod
    def get_sampl_sub_ind(cls):
        return cls.sampl_sub_ind
    
    ## 11
    @classmethod
    def set_sampl_sub_ind(cls, value:int):
        cls.sampl_sub_ind = value

    ## 12
    @classmethod
    def reset_sampl_sub_ind(cls):
        cls.sampl_sub_ind = None

    ## 13
    @classmethod
    def get_other_indxs(cls):
        return cls.other_indxs

    ## 14
    @classmethod
    def set_other_indxs(cls, value):
        cls.other_indxs = value

    ## 15
    @classmethod
    def reset_other_indxs(cls):
        cls.other_indxs = None

    ## 16
    @classmethod
    def get_train_file_path(cls):
        return cls.train_file_path
    
    ## 17
    @classmethod
    def set_train_file_path(cls, value):
        cls.train_file_path = value

    ## 18
    @classmethod
    def reset_train_file_path(cls):
        cls.train_file_path = None

    ## 19
    @classmethod
    def get_test_file_path(cls):
        return cls.test_file_path
    
    ## 20
    @classmethod
    def set_test_file_path(cls, value):
        cls.test_file_path = value

    ## 21
    @classmethod
    def reset_test_file_path(cls):
        cls.test_file_path = None

    ## 22
    @classmethod
    def get_search_type(cls):
        return cls.search_type
    
    ## 23
    @classmethod
    def set_search_type(cls, value):
        cls.search_type = value

    ## 24
    @classmethod
    def reset_search_type(cls):
        cls.search_type = None

    def __init__(self):
        HandleFile.reset_sampl_file_pres_state()
        HandleFile.reset_train_ind()
        HandleFile.reset_test_ind()
        HandleFile.reset_sampl_sub_ind()
        HandleFile.reset_other_indxs()
        HandleFile.reset_train_file_path()
        HandleFile.reset_test_file_path()
        HandleFile.reset_search_type()

    def __call__(self, samp_file_pres=0, upld_w_name=0):
        """
        Inputs:
        samp_file_pres: If there exists sample submission file for the upload
        upld_w_name: Whether to search and upload the data files using their path or index.
        """
        assert samp_file_pres == 1 or samp_file_pres == 0
        assert upld_w_name == 1 or upld_w_name == 0

        self.set_sampl_file_pres_state(value=samp_file_pres)

        if upld_w_name == 0:
            self.data_indxs()
            self.chunk_decide()
            self.set_search_type(value=0)

        else:
            usr_train_fl_name = str(input("Please enter the name of the Train Data File: "))
            usr_test_fl_name = str(input("Please enter the name of the Test Data File: "))

            self.set_train_file_path(value=self.find_files_in_dir(filename=usr_train_fl_name, search_path=os.getcwd()))
            self.set_test_file_path(value=self.find_files_in_dir(filename=usr_test_fl_name, search_path=os.getcwd()))

            self.set_search_type(value=1)

        # Other CSVs to be read
        other_csvs = int(input("Do you have other csvs to be read? 1/0: "))
        if other_csvs == 1:
            self.other_csv_indxs()  

    def print_ind_flname(self, ind_list):
        """
        Prints the Index and the corresponding file name in the directory for a list of indices.
        """
        for indx in ind_list:
            print(f'Index Number: {indx} - File Name: {os.listdir()[indx]}')

    def data_indxs(self):
        """
        Returns the indices of Train, Test and Submission data files.
        """
        # Get the indices of data files based on their extensions
        indices = []
        for ind, i in enumerate(os.listdir()):
            data_f = re.findall(r'csv|xlsx', i)
            if data_f:
                indices.append(ind)

        # Assigning indices based on the presence of Sample Submission File in the directory
        if HandleFile.get_sampl_file_pres_state() == 0:
            temp_ind = []
            for ind in indices:
                train_file = re.findall(r'train'.lower(), (os.listdir()[ind]).lower()) # Train File Index
                if train_file:
                    temp_ind.append(ind)

                test_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if test_file:
                    test_ind = ind

            if len(temp_ind) == 1:
                train_ind = temp_ind[0]
            else:
                print(self.print_ind_flname(ind_list=temp_ind))
                train_ind = int(input('Please Choose the Index from the above list: '))

            HandleFile.set_train_ind(value=train_ind)
            HandleFile.set_test_ind(value=test_ind)
        
        else:
            temp_ind = []

            # From the previous indices, determine the specific indices of those files
            for ind in indices:
                # Searching the files
                train_file = re.findall(r'train'.lower(), (os.listdir()[ind]).lower()) # Train File Index
                if train_file:
                    temp_ind.append(ind)
                
                test_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if test_file:
                    test_ind = ind

                samp_file = re.findall('.+submission'.lower(), (os.listdir()[ind]).lower()) # Sample file Index
                if samp_file:
                    samp_file = ind

            if len(temp_ind) == 1:
                train_ind = temp_ind[0]
            else:
                print(self.print_ind_flname(ind_list=temp_ind))
                train_ind = int(input('Please Choose the Index from the above list: '))

            HandleFile.set_train_ind(value=train_ind)
            HandleFile.set_test_ind(value=test_ind)
            HandleFile.set_sampl_sub_ind(value=samp_file)
        
    def other_csv_indxs(self):
        indices = []
        for ind, i in enumerate(os.listdir()):
            data_f = re.findall(r'csv|xlsx', i)
            if data_f:
                indices.append(ind)

        othr_indxs = [indx for indx in indices if indx not in [HandleFile.get_test_ind(), HandleFile.get_train_ind(), HandleFile.get_sampl_sub_ind()]]

        if len(othr_indxs) != 0:
            HandleFile.set_other_indxs(value=othr_indxs)

        return othr_indxs
    
    def chunk_decide(self):
        """
        Helps in deciding whether or not to use chunking without opening the file
        """
        with open(os.listdir()[HandleFile.get_train_ind()], 'rb') as c_:
            x = len(c_.readlines())-1
            c_.close()

            print(f'{os.listdir()[HandleFile.get_train_ind()]} : {x} rows.')
            
    def find_files_in_dir(self, filename, search_path):
        """
        This function would look for the data files where moving out the contents out of the sub-directory is not feasible.
        """
        for root, dir, files in os.walk(search_path.lower()):
            files = list(map(str.lower, files))
            if filename.lower() in files:
                return os.path.join(root,filename)