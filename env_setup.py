import os
import shutil
import glob
import nbformat as nbf

class Envsetup:
    '''
    This class does the following things:
        1. Create a new Directory for the project.
        2. Copy pathfinder.py to the directory.
        3. Move the data folder (zipped for now) into the newly created directory.
        4. Create a .ipynb file.

    Site Dictionary:
            MH - Machine Hack
            AV - Analytics Vidya
            ZN - Zindi
            KG - Kaggle
    '''

    def __init__(self, site:str, custom_PS:str, zip_fold_pres:str):
        self.site = site
        self.custom_PS = custom_PS
        self.zip_fold_pres = zip_fold_pres
        self.create_dir()
        self.copy_pathfinder()
        self.move_from_dwnload_fld()
        self.create_workbook()


    def create_dir(self):
        '''
        This function creates the directory for a given site
        '''
        # Site Dictionary
        site_dict = {'MH':'MH_dir',
                     'AV':'AV_dir',
                     'ZN':'ZN_dir',
                     'KG':'KG_dir'}

        # Directory Name
        directory = str(input('Please Enter the name of the Folder to be created: '))

        # Parent Directory Path
        for key in site_dict:
            if key == self.site:
                par_dir = os.environ.get(site_dict[key])

        # Path
        global path_dir
        path_dir = os.path.join(par_dir, directory)

        # Dealing with the pre-existence of the directory
        try:
            # Create the Directory
            os.mkdir(path_dir)

             # Print the Confirmation
            print(f'{directory} directory has been created!!')

        except FileExistsError:
            print('Directory already exists with the given namme.')

    def copy_pathfinder(self):
        '''
        This function copies the pathfinder.py file from the source path and pastes it to directory
        '''
        try:
            shutil.copy(os.environ.get('PathFinder'), path_dir)
            print('Path Finder file has been moved into the directory successfully!!')
        except:
            pass

    def move_from_dwnload_fld(self):
        '''
        Moves zipped/unzipped downloaded data folder from the site into the newly created directory.

        By default moves the last folder (the newest file/folder in the download directory.)
        '''
        default_folder = os.environ.get('Download_Folder')

        try:

            if self.zip_fold_pres.lower() == 'n':
                # Finding the .csv files
                files = glob.glob(os.path.join(default_folder, "*.csv"))

                # Sort list of files based on last modification time in descending order
                files_sorted = sorted(files,
                                key=os.path.getmtime,
                                reverse=True)
                
                # Global variable - path
                for file in files_sorted[:2]:
                    shutil.move(file,path_dir)
                
                # Confirmation
                print('Downloaded Data Folder has been moved Successfully!!!')

            else:
                # Finding the zip folders
                files = glob.glob(os.path.join(default_folder, "*.zip"))

                # Sort list of files based on last modification time in descending order
                files_sorted = sorted(files,
                                key=os.path.getmtime,
                                reverse=True)
                
                # Global variable - path
                shutil.move(files_sorted[0],path_dir)

                # Confirmation
                print('Downloaded Data Folder has been moved Successfully!!!')

        except:
            print('Files NOT found!!')


    def create_workbook(self):
        '''
        Creates a Jupyter notebook without having to know the specifics of the file format, JSON schema etc.
        '''
        try:
            # Creating New Workbook
            nb = nbf.v4.new_notebook()

            # Entering the Problem Statement
            text1 = """# Problem Statement\n
            %s
            """%(self.custom_PS)

            # Markdown #2
            text2 = """## Helper Function Connection"""

            # MArkdown #3
            text3 = """# Imports"""

            # Running the PathFinder.py file
            code1 = """import PathFinder as pf\n
            pf.add_path()
            """

            # Adding a Markdown Cell to the created Notebook
            nb['cells'].append(nbf.v4.new_markdown_cell(text1))

            # Adding another Markdown Cell to the created Notebook
            nb['cells'].append(nbf.v4.new_markdown_cell(text2))

            # Adding the Code Cell to the created Notebook
            nb['cells'].append(nbf.v4.new_code_cell(code1))

            # Adding another Markdown Cell to the created Notebook
            nb['cells'].append(nbf.v4.new_markdown_cell(text3))

            # Finalizing the Schema
            nbf.write(nb, 'Initial.ipynb')

            # Confirming the Notebook Creation
            print('Notebook has been created successfully!!')

            # Moving the created notebook the directory created
            shutil.move('Initial.ipynb', path_dir)

        except:
            print('IPYNB file was not created and moved to the working directory!!!')


if __name__ == '__main__':
    Envsetup(site=input('Please Enter the Site MH/AV/ZN/KG: '),
             zip_fold_pres=input('Please Confirm the presence of zip folder or individual y/n: '),
             custom_PS=input('Please Enter the Case specic Problem Statement: ')) 