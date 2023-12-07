# Imports
import os
import re
import shutil
from zipfile import ZipFile
import sys

class HandleFile:
    """
    Class handles the following processes:
        1. Un-zips the zip folder downloaded from the site.
        2. Moves the unzipped folder/ contents of the zipped folder into the working directory.
        3. Removes the unzipped folder.
        4. Provides the indices of the train and test data file to the child class.
    """
    # Initial State
    class_samp_file:str = None
    train_ind:int = None
    test_ind:int = None
    sampl_sub_ind:int = None
    
    def __init__(self, is_zip:str):

        # Resetting the Value of Class Variable
        HandleFile.reset_sampl_file_pres_state()
        HandleFile.reset_train_ind()
        HandleFile.reset_test_ind()
        HandleFile.reset_sampl_sub_ind()

        # Determine the existence of the zip file and unzip it
        self.is_zip = is_zip
        if self.is_zip.lower()=='y':
            self.unzipFF()
            print('--'*20)

            # Dealing with the Presence of Un-zipped Folder
            unzip_fold = str(input('Un-zipped Folder Exists? (Y/N)')).lower()
            print('--'*20)

            if unzip_fold == 'y':
                org = input("Please Enter the Path of the un-zipped folder: ")
                self.zip_cont_mov(org)
                print('--'*20)

            else:
                pass

        else:
            pass
        
        # Handling the Indices of the Data Files
        samp_file_pres:str = input('Is there a Submission File? Y/N: ').lower()
        HandleFile.set_sampl_file_pres_state(value=samp_file_pres)
        
        self.data_ind()
        
        # Determining the size of the Train Dataset for Upload decision
        print('--'*20)
        print(HandleFile.chunk_decide(f_name=os.listdir()[HandleFile.train_ind]))
        print('--'*20)

    # Class Methods
    ##1
    @classmethod
    def get_sampl_file_pres_state(cls):
        return cls.class_samp_file
    
    ##2
    @classmethod
    def set_sampl_file_pres_state(cls,value:str):
        cls.class_samp_file = value

    ##3
    @classmethod
    def reset_sampl_file_pres_state(cls):
        'To return the state of the variable into its original state'
        cls.class_samp_file = None

    ##4
    @classmethod
    def get_train_ind(cls):
        return cls.train_ind
    
    ##5
    @classmethod
    def set_train_ind(cls, value:int):
        cls.train_ind = value

    ##6
    @classmethod
    def reset_train_ind(cls):
        cls.train_ind = None

    ##7
    @classmethod
    def get_test_ind(cls):
        return cls.test_ind
    
    ##8
    @classmethod
    def set_test_ind(cls, value:int):
        cls.test_ind = value

    ##9
    @classmethod
    def reset_test_ind(cls):
        cls.test_ind = None

    ##10
    @classmethod
    def get_sampl_sub_ind(cls):
        return cls.sampl_sub_ind
    
    ##11
    @classmethod
    def set_sampl_sub_ind(cls, value:int):
        cls.sampl_sub_ind = value

    ##12
    @classmethod
    def reset_sampl_sub_ind(cls):
        cls.sampl_sub_ind = None

    def unzipFF(self):
        ''' 
        Locates a File (w/ .zip extension) in the working directory. Unzips it, and the contents are then saved in the same directory.
        '''
        # Locate the zip file in the folder
        for ind, i in enumerate(os.listdir()):
            zfs = re.findall("zip\Z", i)
            if len(zfs) != 0:
                folder_ind = ind
                # Unzip and Display the contents of the zip folder
                z = ZipFile(os.listdir()[folder_ind], 'r')
                z.printdir()
                z.extractall()
                z.close()


    def zip_cont_mov(self,org, targ=os.getcwd(), del_dir=True):
        '''
        Take out the files from the unzipped folder into the working directory and then delete the orgin folder
        '''
        # Fetching the list of all the files
        files = os.listdir(os.path.join(targ, org))
        # Fetching all the files to directory
        for f in files:
            shutil.move(org + f, targ)
        print('Files have been moved out of the un-zipped folder.')
        # Delete the Folder after the files are moved
        if del_dir:
            shutil.rmtree(org)
            print('The un-zipped folder has been removed from the directory.')


    @staticmethod
    def chunk_decide(f_name:str):
        '''
        Helps in deciding whether or not to use chunking without opening the file
        '''
        with open(f_name,'rb') as f_:
            x = len(f_.readlines())-1 
            # 1 has been deducted from the length in order to account for the header
            file_size = sys.getsizeof(f_)
            f_.close()
            
        print(f'Number of rows of the file: {x:_}')
        print(f'Size of the File is: {file_size/1024} GB')

    def print_ind_flname(self, ind_list):
        """
        Prints the Index and the corresponding file name in the directorry for a list of indices.
        """
        for indx in ind_list:
            print(f'Index Number: {indx} - File Name: {os.listdir()[indx]}')

    def data_ind(self):
        '''
        Returns the indices of Train, Test and Submission data files.
        '''

        # Get the indices of data files based on their extensions
        indices = []
        for ind, i in enumerate(os.listdir()):
            data_f = re.findall(r'csv|xlsx', i)
            if data_f:
                indices.append(ind)

        if HandleFile.get_sampl_file_pres_state() == 'n':

            temp_tr_ind = [] # Temporary Training Index List

            # From the previous indices, determine the specific indices of those files
            for ind in indices:
                # Searching the files
                train_file = re.findall(r'train'.lower(), (os.listdir()[ind]).lower()) # Train File Index
                if train_file:
                    temp_tr_ind.append(ind)
                
                test_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if test_file:
                    test_ind = ind

            if len(temp_tr_ind) == 1:
                train_ind = temp_tr_ind[0]
            else:
                print(self.print_ind_flname(ind_list=temp_tr_ind))
                train_ind = int(input('Please Choose the Index from the above list: '))
                

            HandleFile.set_train_ind(value=train_ind)
            HandleFile.set_test_ind(value=test_ind)

            return train_ind, test_ind

        else:

            temp_tr_ind = [] # Temporary Training Index List

            # From the previous indices, determine the specific indices of those files
            for ind in indices:
                # Searching the files
                train_file = re.findall(r'train'.lower(), (os.listdir()[ind]).lower()) # Train File Index
                if train_file:
                    temp_tr_ind.append(ind)
                
                test_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if test_file:
                    test_ind = ind

                samp_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if samp_file:
                    samp_file = ind

            if len(temp_tr_ind) == 1:
                train_ind = temp_tr_ind[0]
            else:
                print(self.print_ind_flname(ind_list=temp_tr_ind))
                train_ind = int(input('Please Choose the Index from the above list: '))

            HandleFile.set_train_ind(value=train_ind)
            HandleFile.set_test_ind(value=test_ind)
            HandleFile.set_sampl_sub_ind(value=samp_file)

            return train_ind, test_ind, samp_file