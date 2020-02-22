# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:05:22 2019

Deloitte module dependencies:
    data 1.0
    prompt 1.0

Front-end flow and input control enabling non-Python users to utlise a Python
to SQL connection for batch uploading standardised data from excel or csv.

Speed-up:
Large batch imports can save significant amounts of time by automating with
this code. Very fast imports are achievable with xls, xlsm and csv extensions,
xlsx is slower but still faster than manual upload.
_______________________________________________________________________________

v1.0 | [11/08/2019] | developer: James Briggs | reviewed by: name

Establish multiple uploads using a combination of directory paths and file
paths using the AND syntax. Sheetnames (for excel) and server details are
optional arguments accessed using the @ syntax. Users can view version details
by typing 'version' and also get help with each input by typing 'help'. All
data is uploaded as string and blank values are replaced by NULL, this helps
prevent datatype problems after SQL import.
_______________________________________________________________________________

"""
from os.path import isdir, isfile, splitext
from os import walk
import sys  # comment out this and following line before compiling
sys.path.insert(0, r'K:\A & A\London\FS\Clients\S\Securitisation\A&M'
                   r'\User folders\James Briggs\Py Tools\lib')
from data import Sql
from prompt import go

# initialise prompt object with application details
Q = go("Excel2SQL", version="1.0", author="James Briggs",
       email="jamesbriggs@deloitte.co.uk", detail="Application used to " +
       "quickly upload Excel or CSV files to MS SQL Server.")

# ask user which database to connect to
DATABASE = Q.ask("Database", "The database variable refers to the SQL " +
                 "database you would like to use, eg 'Client04'. If using " +
                 "an alternative server, use the following format = " +
                 "'Database@Server'.")

SERVER = "UKVIR10305,50555"  # default server name

# checking if user added server detail
if "@" in DATABASE:
    DATABASE, SERVER = DATABASE.split("@")

# setting up the connection, automatically assumes UKVIR10305,50555 for the
# server, change this via Jupyter notebook using the 'server' argument
DT = Sql(DATABASE, SERVER)

RUN = True  # initialise run variable

# this section will rerun so we can easily restart if use enters wrong input
while RUN:
    # ask user for input data directory
    LOC = Q.ask("Path", "This is the filepath to the file you would" +
                " like to import, this should include the filename and file " +
                "extension. If you are importing multiple files, use the " +
                "following format = 'filepath1 AND filepath2 AND filepath3' " +
                "until all files are included. If you want to upload all " +
                "files (xlsx, xlsm, xls, csv and txt only) within a " +
                "directory, include the directory path only.\n\nBoth options" +
                " allow for a sheetname to be specified (Excel formats only)" +
                ". To do this, use the following format = 'Sheet@Path'.")

    SHEET = 0  # initialise sheet variable

    # compile into list (incase of AND being used) to loop through
    if " AND " in LOC:
        # split into seperate statements
        LOC = LOC.split(" AND ")
    else:
        # if not we put into single list anyway for following for-loop
        LOC = [LOC]

    # starting for-loop for the list (single or multi) of inputs
    for path in LOC:
        # checking if user added server detail
        if "@" in path:
            SHEET, path = path.split("@")

        # check if file or directory
        if isfile(path):
            # uploading the file to the specified SQL location, we use the
            # filename as the table name, another argument 'batchsize' can be
            # adjusted via Jupyter

            DT.push_raw(path, sheet=SHEET)
            # now compile into string for final details print
            loc_str = "\n".join(path)
            # update the user
            print("Data upload completed. See the following details:\n" +
                  "Server: " + SERVER + "\n" +
                  "Database: " + DATABASE + "\n" +
                  "Filepath(s):\n" + path + "\n")
            RUN = False  # once complete, we want to break the while loop

        elif isdir(path):
            dirpath, filename_list = None, None  # initialise vars that we use
            # get list of files in target location
            for (dirpath, _, filename_list) in walk(path):
                break  # this stops us going more than one layer deep

            # how many files have we found?
            print(str(len(filename_list)) + " files found, some may not be " +
                  "valid filetypes.")

            # loop through all filenames
            f_count = 0  # initialise valid filename count
            valid = ['.xlsx', '.xlsm', '.xls', '.csv']  # need to add txt
            for filename in filename_list:
                # get extenstion and check validity AND check is not temp file
                if splitext(filename)[1] in valid and filename[:2] != '~$':
                    # push file to SQL
                    try:
                        DT.push_raw(dirpath+"\\"+filename, sheet=SHEET)
                        # increase valid file count
                        f_count += 1
                    except Exception as error:
                        # if we get some error for a single file, we should
                        # still upload the remaining
                        print("Upload failed for '"+filename+"'\nError: " +
                              str(error)+"\n")
                else:
                    pass  # if not a valid filename we pass

            print("Data upload completed. See the following details:\n" +
                  "Server: " + SERVER + "\n" +
                  "Database: " + DATABASE + "\n" +
                  "Directory:\n" + dirpath + "\n" +
                  str(f_count) + " files uploaded.")
            RUN = False

        else:
            # if user types in incorrect filepath, let them know and try again
            print("File not found, please try again.\n")
            RUN = True
            break

input("Press anything to quit.\n")
