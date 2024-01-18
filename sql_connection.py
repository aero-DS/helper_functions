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

    ## Creating Table(s)

    def mult_tables(self):
        """
        For a given set of csv files in the working directory, creates a sql table for the csv file.
        """
        csv_names = []
        for ind, i in enumerate(os.listdir()):
            data_f = re.findall(r'csv|xlsx', i)
            if data_f:
                csv_names.append(i)

        for csv_ in csv_names:
            print(f"The Current File Name is: {csv_}")
            csv_upl = int(input("Do you wish to upload the current csv file? 1/0: "))
            
            if csv_upl == 0:
                continue
            else:
                tbl_name = str(input("Enter the desired Table Name: "))
                self.create_sqltable_from_csv(csv_name=csv_, table_name=tbl_name)

    
    def create_sqltable_from_csv(self, csv_name, table_name):
        """
        Generates SQL queries to create tables for each of the csv file.
        """
        import pandas as pd

        # Reading the First Row of the Dataframe
        df = pd.read_csv(csv_name, nrows=1)

        # SQL table creation creation statement
        df_cols = df.columns
        df_dtypes = df.dtypes
        sql_cols = []

        for col, data_dtype in zip(df_cols, df_dtypes):
            if "int" in str(data_dtype):
                sql_cols.append(f"{col} INT")
            elif "float" in str(data_dtype):
                sql_cols.append(f"{col} FLOAT")
            elif "date" in str(data_dtype):
                sql_cols.append(f"{col} DATETIME")
            else:
                sql_cols.append(f"{col} VARCHAR(255)")

        # Create the SQL Table Statement
        sql_tbl_statemnt = f"CREATE TABLE {table_name} ({', '.join(sql_cols)});"

        # Execution
        self.stat_query_exec(query=sql_tbl_statemnt)

    # Existing Database
    def create_exc_conn(self, exc_dbname):
        """
        Creates a connection with an existing Database
        """
        return mc.connect(
            host = self.host_name,
            user = self.user_name,
            password = os.environ.get('Root_password'),
            database = exc_dbname)
    
    # Static Queries
    def stat_query_exec(self, query):
        """
        Executes static sql statements (creating tables) for the newly created database.
        """
        with self.create_exc_conn(exc_dbname=self.exc_dbname) as conn:
            mycursor = conn.cursor()
            mycursor.execute(query)

    # Dynamic Queries
    def dynamic_query(self):
        """
        This function provides dynamic query option for both new and existing databases.
        """
        nxt_query = 1

        while nxt_query == 1:

            with self.create_exc_conn(exc_dbname=self.exc_dbname) as conn:
                mycursor = conn.cursor()
                query = str(input("Input Query: "))
                mycursor.execute(query)

            nxt_query = int(input("Any Further Query? 1/0:  "))