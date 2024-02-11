# Imports

from env_setup import *

# Execution
if __name__ == "__main__":
    try:
        proj = EnvSetup()
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

        # Checking the presence of Data Files in the mentioned folder location for the given date
        decs_afterline()
        dt_lkup_cnf = int(input("Do you want to select today's date for folder filter? 1/0: "))
        assert dt_lkup_cnf == 1 or dt_lkup_cnf == 0, "Only takes values 1/0"

        if dt_lkup_cnf == 1:
            fold_files = proj.conf_data_files(targ_fold=proj.data_fold, targ_dt=str(datetime.date.today()))
            
        else:
            cust_dt = str(input("Please enter the date for filtering folders in YYYY-MM-DD: "))
            fold_files = proj.conf_data_files(targ_fold=proj.data_fold, targ_dt=cust_dt)
            print(fold_files)

        decs_afterline()
        files_fnd = int(input("Did you find the concerned files? 1-Yes /0-No: "))
        assert files_fnd == 1 or files_fnd == 0, "Only takes values 1/0/"

        if files_fnd == 0:
            cust_dt = str(input("Please enter a different date in YYYY-MM-DD: "))
            fold_files = proj.conf_data_files(targ_fold=proj.data_fold, targ_dt=cust_dt)

        decs_afterline()
        print(EnvSetup.site_dict)
        site_name = str(input("Please Enter the name of the site from where the project will be done: ")).upper()
        proj_fold_name = str(input("Please enter the name of the directory to be created: "))
        proj.create_proj_dir(ky=site_name, dir_title=proj_fold_name)
        print(f'Project Directory has been created.')

        decs_afterline()
        proj.copy_helperFunc()
        print("Helper Function file has been copied into the project directory.")

        decs_afterline()
        proj.mov_data_files(files_in_dir=fold_files)
        
        decs_afterline()
        print(f'Dictionary for the templates to be copied into the project directory: ')
        print(proj.ipnyb_templt_dict)
        templt_ky = input("Please enter the template key from the above dictionary: ").upper()
        proj.copy_ipnyb_templt(proj_type=templt_ky)
        print("Template file has been copied into the Project Directory.")

        
    except AssertionError:
        print("Please Check for the data types for the variables associated with the assert statement")

    except FileNotFoundError:
        print("Please Check for the presence of the file in the directory.")

    except:
        print("BIG FAIL!!!!")

    else:
        print("Setting-up the project directory has been completed.")