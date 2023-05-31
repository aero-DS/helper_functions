# Imports
import os
import re
import shutil
from zipfile import ZipFile

class HandleFile:
    """
    Class handles the following processes:
        1. Un-zips the zip folder downloaded from the site.
        2. Moves the unzipped folder/ contents of the zipped folder into the working directory.
        3. Removes the unzipped folder.
        4. Provides the indices of the train and test data file to the child class.
    """
    
    def __init__(self, is_zip=True, samp_file_pres=False):

        # Determine the existence of the zip file and unzip it
        self.is_zip = is_zip
        if self.is_zip:
            HandleFile.unzipFF()
        print('--'*20)

        # Dealing with the Presence of Un-zipped Folder
        unzip_fold = str(input('Un-zipped Folder Exists? (Y/N)')).lower()
        print('--'*20)
        if unzip_fold == 'y':
            org = input("Please Enter the Path of the un-zipped folder: ")
            HandleFile.zip_cont_mov(org)
        print('--'*20)

        # Handling the Indices of the Data Files
        self.samp_file_pres=samp_file_pres
        if self.samp_file_pres:
            HandleFile.data_ind(samp_fil_ind=self.samp_file_pres)
        else:
             HandleFile.data_ind(samp_fil_ind=self.samp_file_pres)

    @staticmethod
    def unzipFF():
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

    @staticmethod
    def zip_cont_mov(org, targ=os.getcwd(), del_dir=True):
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
        with open(f_name) as f_:
            x = len(f_.readlines())-1 
            # 1 has been deducted from the length in order to account for the header
            f_.close()
            print(f'Number of rows of the file: {x:_}')

    @staticmethod
    def data_ind(samp_fil_ind=False):
        '''
        Returns the indices of Train, Test data files.
        '''

        # Get the indices of data files based on their extensions
        indices = []
        for ind, i in enumerate(os.listdir()):
            data_f = re.findall(r'csv|xlsx', i)
            if data_f:
                indices.append(ind)

        if samp_fil_ind == False:
            # From the previous indices, determine the specific indices of those files
            for ind in indices:
                # Searching the files
                train_file = re.findall(r'train'.lower(), (os.listdir()[ind]).lower()) # Train File Index
                if train_file:
                    train_ind = ind
                
                test_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if test_file:
                    test_ind = ind

            return train_ind, test_ind

        else:
            # From the previous indices, determine the specific indices of those files
            for ind in indices:
                # Searching the files
                train_file = re.findall(r'train'.lower(), (os.listdir()[ind]).lower()) # Train File Index
                if train_file:
                    train_ind = ind
                
                test_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if test_file:
                    test_ind = ind

                samp_file = re.findall(r'test'.lower(), (os.listdir()[ind]).lower()) # Test file Index
                if samp_file:
                    samp_file = ind

            return train_ind, test_ind, samp_file
        
    