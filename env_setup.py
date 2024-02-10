# Libraries
import configparser
import shutil
import dir_paths as dp
import os
import datetime

# Supplement Functions
def decs_afterline():
    print("--"*20)

def read_config(sec, ky):
    """
    Extracts values for the given key from the relevant section.
    """
    parent_path = dp.config_path
    file_name = 'config.ini'
    
    config = configparser.ConfigParser()
    config.read(os.path.join(parent_path,file_name))
    val = config[sec][ky]
    return val

# Working Class
class EnvSetup:
    """
    This class performs the following tasks:
        1. Checks for the presence of downloaded data files for the project.
        2. Creates the project specific directory.
    """

    def __init__(self):
        EnvSetup.rst_data_fold()
        EnvSetup.rst_proj_par_dir()
        EnvSetup.rst_same_dir_name()

    ## Class Variables
    
    # Template Dictionary
    ipnyb_templt_dict = {
        'CV' : 'Computer_Vision_template.ipynb',
        'Reg' : 'Regression_template.ipynb'
    }
    
    # Site Dictionary
    site_dict = {
        'MH' : 'Machine Hack',
        'AV' : 'Analytics Vidya',
        'ZN' : 'Zindi',
        'KG' : 'Kaggle',
    }

    # Default Directory for the project
    proj_par_dir = None

    @classmethod
    def rst_proj_par_dir(cls):
        "Resets the value of the path for the Project Directory."
        EnvSetup.proj_par_dir = None

    @classmethod
    def set_proj_par_dir(cls, val):
        "Sets the value of the path for the Project Directory"
        EnvSetup.proj_par_dir = val

    @classmethod
    def get_proj_par_dir(cls):
        "Returns the path set for the directory containing the Project Directory."
        return cls.proj_par_dir

    # Default Directory for Downloaded Data Files
    data_fold = None

    @classmethod
    def rst_data_fold(cls):
        "Resets the value of the path for the data files."
        EnvSetup.data_fold = None

    @classmethod
    def set_data_fold(cls, val):
        "Sets the value of the path for the data files"
        EnvSetup.data_fold = val

    @classmethod
    def get_data_fold(cls):
        "Returns the path set for the directory containing the data files."
        return cls.data_fold
    
    # Same Name Directory Existence Confirmation (0:Unique Dir Name / 1:Duplicate Dir Name)
    same_dir_name = None

    @classmethod
    def rst_same_dir_name(cls):
        "Resets the value of the same_dir_name"
        EnvSetup.same_dir_name = None

    @classmethod
    def set_same_dir_name(cls, val):
        "Sets the value of the same_dir_name"
        EnvSetup.same_dir_name = val

    @classmethod
    def get_same_dir_name(cls):
        "Returns the value of same_dir_name."
        return cls.same_dir_name

    def conf_data_files(self, targ_fold, targ_dt):
        """
        This function performs the following tasks:
            1. Checks the presence of the downloaded data files in the specified directory (based on the date the files were created.)
            2. 
        """
        cr_files = []
    
        for file in os.listdir(targ_fold):
            file_path = os.path.join(targ_fold, file)
            create_time = os.path.getctime(file_path)
            create_date = datetime.datetime.fromtimestamp(create_time).date()
            if str(create_date) == targ_dt:
                cr_files.append(file)
            
        return cr_files
    
    # HAVING ISSUES
    def mov_data_files(self, files_in_dir):
        """
        Moves the downloaded data folder/files from the default foldrs into the project directory.
        """
        try:
            print('Indices of the files in the directory are:\n')
            for ind,f in enumerate(files_in_dir):
                print(f'{ind} : {f}')

            moving_conf = int(input("Do you want to move all the listed files into the project directory? 1/0: "))
            assert moving_conf == 1 or moving_conf == 0, "Please Enter only from the provided Options"

            if moving_conf == 1:
                for file in files_in_dir:
                    file_src = os.path.join(EnvSetup.get_data_fold(),file)
                    file_dst = os.path.join(EnvSetup.proj_par_dir(),file)
                    shutil.move(file_src, EnvSetup.proj_par_dir())

            else:
                fil_indxs = list(input("Please Enter the Indices of the files you want moved.: "))
                for ind in sorted(fil_indxs, reverse=True):
                    file_src = os.path.join(EnvSetup.get_data_fold(),files_in_dir[ind])
                    file_dst = os.path.join(EnvSetup.proj_par_dir(),files_in_dir[ind])
                    shutil.move(file_src, file_dst)

        except:
            print(f'Data Folder/File have not been moved into the directory.')


    def create_proj_dir(self, ky, dir_title):
        '''
        This function creates the directory for a given site

        Inputs:
            ky: Key from the class dictionary site_dict
            dir_title: Name of the folder contianing the relevant project
        '''
        EnvSetup.set_proj_par_dir(val=os.path.join(read_config(sec='Site_Directories', ky=ky),dir_title))

        os.mkdir(EnvSetup.get_proj_par_dir())

    def copy_helperFunc(self):
        '''
        This function copies the python file for the custom function into the project directory.
        '''
        src = read_config(sec='Base_Directories', ky='pathFinder')
        dst = os.path.join(EnvSetup.get_proj_par_dir(),'PathFinder.py')
        shutil.copy(src, dst)

    def copy_ipnyb_templt(self, proj_type):
        """
        Copies case-specific templates into the project directories
        """
        templt_file = os.path.join(read_config(sec='Base_Directories', ky='ipnyb_templates'), EnvSetup.ipnyb_templt_dict[proj_type])
        dst = os.path.join(EnvSetup.get_proj_par_dir(),'Main.ipynb')
        shutil.copy(templt_file, dst)