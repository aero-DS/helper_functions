# Imports

from env_setup import *

# Execution
if __name__ == "__main__":
    try:
        proj = EnvSetup()

        # Establishing the Path for Data Folders/Files
        decs_afterline()
        dflt_fold_pos_conf = int(input("Are your download files in the Download directory? 1/0: "))
        assert dflt_fold_pos_conf == 1 or dflt_fold_pos_conf == 0, "Only takes values 1/0."

        if dflt_fold_pos_conf == 1:
            proj.set_data_fold(val=read_config(sec='Base_Directories', ky='deflt_file_dwnld'))
            print("Path to the Data Files directory has been updated successfully!!")

        else:
            cust_data_fld = input("Please enter the path of the directory containing the data files: ")
            proj.set_data_fold(val=cust_data_fld)
            print("Path to the Data Files directory has been updated successfully!!")

        # Create Project Directory
        decs_afterline()
        print(EnvSetup.site_dict)
        site_name = str(input("Please Enter the name of the site from where the project will be done: ")).upper()

        decs_afterline()
        print("List of Directories already present in the site directory: ")
        proj.show_site_directories(site=site_name)

        decs_afterline()
        proj_fold_name = str(input("Please enter the name of the directory to be created: "))
        proj.create_proj_dir(ky=site_name, dir_title=proj_fold_name)
        print(f'Project Directory has been created.')

        # Copying the Helper Function into the Project Directory
        decs_afterline()
        proj.copy_helperFunc()
        print("Helper Function file has been copied into the project directory.")

        # Checking the presence of Data Files in the mentioned folder location for the given date
        decs_afterline()
        dt_lkup_cnf = int(input("Do you want to select today's date for folder filter? 1/0: "))
        assert dt_lkup_cnf == 1 or dt_lkup_cnf == 0, "Only takes values 1/0"

        if dt_lkup_cnf == 1:
            fold_files = proj.conf_data_files(targ_fold=proj.get_data_fold(), targ_dt=str(datetime.date.today()))
            print(fold_files)

        else:
            cust_dt = str(input("Please enter the date for filtering folders in YYYY-MM-DD: "))
            fold_files = proj.conf_data_files(targ_fold=proj.get_data_fold(), targ_dt=cust_dt)
            print(fold_files)

        decs_afterline()
        files_fnd = int(input("Did you find the concerned files? 1/0: "))
        assert files_fnd == 1 or files_fnd == 0, "Only takes values 1/0"

        # TO BE REFACTORED
        if files_fnd == 0:
            pass

        else:
            decs_afterline()
            proj.mov_data_files(files_in_dir=fold_files)

        # Copying the ipynb templates into the Project Directory
        decs_afterline()
        print(f'Dictionary for the templates to be copied into the project directory: ')
        print(proj.ipnyb_templt_dict)
        templt_ky = input("Please enter the template key from the above dictionary: ").upper()
        proj.copy_ipnyb_templt(proj_type=templt_ky)
        print("Template file has been copied into the Project Directory.")

        # Unzipping the Data Folder and moving the contents of the file if required
        decs_afterline()
        unzip_file = int(input("Do you have to unzip the data folder? 1/0: "))
        if unzip_file == 1:
            proj.mov_zimovout_zip_contp_cont(projct_dir=proj.get_proj_par_dir())
    
    except AssertionError:
        print("Please Check for the data types for the variables associated with the assert statement")

    except FileNotFoundError:
        print("Please Check for the presence of the file in the directory.")

    except:
        print("BIG FAIL!!!!")

    else:
        print("Setting-up the project directory has been completed.")