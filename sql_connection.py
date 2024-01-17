import mysql.connector as mc
import os
import configparser
import dir_paths as dp
import re

class CreateConnDb:
    """
    This class performs the following tasks:
        1. Creates a MySql connection
        2. Creates a Database.
        3. Gives the headers of the files with their respective names.
    """

    # Class Dictionary

    def __init__(self):

        sect = input("Enter the Concerned Section for the look-up: ")

        self.host_name = self.read_config(sec=sect, ky='hostname')
        self.user_name = self.read_config(sec=sect, ky='user_name')

        db_creation = str(input('Do you want to create a New Database? Y/N: '))

        if db_creation.lower() == 'y':
            print('List of Databases: ')
            self.check_dbnames()
            self.dbname = str(input("Enter the Name of the Database to be Created: "))
            self.create_db(db_name=self.dbname)

        else:
            self.exc_dbname = str(input("Enter the Name of the Existing Database: "))
            self.create_exc_conn(exc_dbname=self.exc_dbname)

    def read_config(self, sec, ky):
        """
        Extracts values for the given key from the relevant section.
        """
        parent_path = dp.config_path
        file_name = 'config.ini'
        
        config = configparser.ConfigParser()
        config.read(os.path.join(parent_path,file_name))
        val = config[sec][ky]
        return val
    
    def files_head_dict(self):
        """
        Returns a dictionary containing the name of the name of the file with their respective headers.
        """
        file_headers_dict = dict()

        for _, i in enumerate(os.listdir()):
            data_f = re.findall(r'csv|xlsx', i)
            if data_f:
                with open(i,'r') as f:
                    x = f.readlines()[0]
                    file_headers_dict.update({i:x})
                    f.close()

        return file_headers_dict

    # New DataBase
    def create_nw_conn(self):
        """
        Creates the MySQL connection.
        """
        return mc.connect(
            host = self.host_name,
            user = self.user_name,
            password = os.environ.get('Root_password'))
    
    def check_dbnames(self):
        """
        Checks the presence of the existing database with the same given name
        """
        with self.create_nw_conn() as conn:
            mycursor = conn.cursor()
            query = "SHOW DATABASES"
            mycursor.execute(query)

            for dbs in mycursor:
                print(dbs)

    def create_db(self, db_name):
        """
        Creates a DB with the MySql connection.
        """
        with self.create_nw_conn() as conn:
            mycursor = conn.cursor()
            query = "CREATE DATABASE {0}"
            f_query = query.format(db_name)
            mycursor.execute(f_query)

    # Existing Database
    def create_exc_conn(self, exc_dbname):
        """
        Creates a connection with an existing Database
        """
        return mc.connect(
            host = self.host_name,
            user = self.user_name,
            password = os.environ.get('Root_password'),
            database = self.exc_dbname)
    
    # Dynamic Query
    def dynamic_query(self):
        """
        This function provides dynamic query option for both new and existing databases.
        """
        nxt_query = 1

        while nxt_query == 1:

            with self.create_nw_conn() as conn:
                mycursor = conn.cursor()
                query = str(input("Input Query: "))
                mycursor.execute(query)

            nxt_query = int(input("Any Further Query? 1/0:  "))