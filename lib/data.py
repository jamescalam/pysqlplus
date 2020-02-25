# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:04:24 2019

Data library to be used as source code for business specific data
manipulation tasks.
_______________________________________________________________________________

v1.0 | [18/08/2019] | developer: James Briggs | reviewed by: name

Sql class complete with the [get_list, get_cols, get_table, push_dataframe,
push_raw, union, drop, manual, nullify] functions.
Supports xlsx, xlsm, xls, csv filetypes for upload. Can download SQL table to
Python dataframe. Quick functions such as table union and drop built in, manual
functions can be built and executed. Simple data pre-processing.
_______________________________________________________________________________

"""

from os import getcwd
from os.path import basename, splitext, expanduser
from datetime import datetime
from pandas import read_csv, read_sql, read_excel
import pyodbc
import urllib
import sqlalchemy


def pull_txt(path):
    pass


def pull_excel(path, sheets=True):
    """
    Function used to import an Excel workbook into a Pandas Dataframe object.

    Parameters
    ----------
    path: Full filepath to file to be imported, including filename and
    file extension.
    sheets: Specifies sheets to import. Must be either True (for all sheets),
        a list of strings (specifying sheetnames), a list of integers
        (specifying the index value of each sheet), or a single string or
        integer, specifying sheetname or index respectively.

    Outputs
    -------
    data: A single Pandas DataFrame object if a single sheet specified, else
        a dictionary containing a Pandas DataFrame object for each sheet.
    """
    # determine extraction method depending on sheets, if list of 
    if sheets:
        # import ALL sheets
        pass
    elif type(sheets) is list:
        df = {}  # initialise dictionary which will contain dataframe objects
        for sheet in sheets:
            # determine whether to use sheet name or sheet index
            if type(sheet) is int:
                df[str(sheet)] = read_excel(path, sheet=sheet)
            elif type(sheet) is str:
                # loop through sheets in workbook and when finding correct...
                # ... sheetname, break and import on that index
                for i in len(0):
                    raise OSError('Sheet read and import function not built.')
            else:
                raise TypeError("'sheets' parameter must be a boolean value "
                                "of 'True' (reads all sheets), a list of "
                                "strings and/or integers, or a single string "
                                f"or integer. A list containing a "
                                "'{type(sheet)}' datatype was given.")
    elif type(sheets) is int:
        pass
    elif type(sheets) is str:
        pass
    else:
        raise TypeError("'sheets' parameter must be a boolean value of 'True' "
                        "(reads all sheets), a list of strings and/or "
                        "integers, or a single string/integer. A "
                        f"'{type(sheet)}' datatype was given.")


def pull_csv(path):
    pass


def pull_oracle(path):
    pass


def auto_reader(path):
    """
    Function used to import a file into a Pandas DataFrame object and
    automatically determine filetype and delimiter.

    Parameters
    ----------
    path: Full filepath to file to be imported, including filename and
    file extension.
    """
    # get file extension from file path
    ext = path.split('.')[-1].lower()

    # check and import if supported filetype, else raise error
    print(f'Importing {ext} file.')  # update user
    if ext == 'txt':
        raise OSError('Function call to pull_txt function to be built.')
    elif 'xls' in ext:
        raise OSError('Function call to pull_excel function to be built.')
    elif ext == 'csv':
        raise OSError('Function call to pull_csv function to be built.')
    elif ext == 'orc':
        raise OSError('Function call to pull_oracle function to be built.')
    else:
        raise OSError(f"'{ext}' file extensions are not supported.")


def prep_for_csv(df, delimiter=','):
    """
    Function used to clean a dataframe before exporting to csv. This helps us
    avoid double delimiters, ex: GBP | 23,000 if exported as csv with comma
    delimiters would split the second column, creating three columns.

    Parameters
    ----------
    df: Pandas dataframe object that we would like to clean.
    delimiter: Specifies the character (or list of characters) to be removed.
        Defaults to ','.
    """
    # first we convert the delimiter string/list into our replace dictionary
    if type(delimiter) is list:
        rep_dict = {}  # initialise replacements dict
        for char in delimiter:
            rep_dict[char] = ''  # set delimiter character to map to nothing

    elif type(delimiter) is str:
        rep_dict = {delimiter: ''}  # map replacement delimiter to nothing

    else:
        raise TypeError("'delimiter' parameter must either be a string or "
                        f"a list of strings. {type(delimiter)} type given "
                        "instead.")

    cols = list(df)  # get list of column names in dataframe

    # replace all instances of the character(s) chosen
    df[cols] = df[cols].replace(rep_dict, regex=True)

    # return clean data
    return df


class Sql:
    """Class used for establishing a Python to Microsoft SQL Server connection
    and import/export/manipulation of data files inside the server.
    """
    def __init__(self, database, server="UKVIR10305,50555"):
        """Here we are initialising our database and server parameters and
        our connection to SQL server.

        Parameters
        ----------
        database: The SQL database name, eg 'Client04'.
        server: The SQL server, defaults to 'UKVIR10305,50555'.
        """
        # database (eg Client01) and server parameters
        self.database = database
        self.server = server

        # here we are telling python what to connect to (our SQL Server)
        self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+self.server+";"
                                   "Database="+self.database+";"
                                   "Trusted_Connection=yes;")
        print("Setup connection for {} on {} server.".format(self.database,
                                                             self.server))

        # initialise query attribute
        self.query = "-- {}\n\n-- Made in Python".format(datetime.now()
                                                         .strftime("%d/%m/%Y"))

    def get_list(self):
        """Returns a list of all tables in the current connection.
        Note that this will also return views and system views.
        """
        # create execution cursor
        cursor = self.cnxn.cursor()
        # initialise list
        tables = []
        for row in cursor.tables():
            tables.append(row.table_name)
        return tables

    def get_cols(self, table):
        """Returns a list of columns in the table specified.

        Keyword arguments:
        table -- the name of the table in SQL server that we want a column
                 list for.
        """
        # get a dataframe of just the columns from SQL
        cols = self.manual("SELECT TOP(0) * FROM [dbo].["+table+"]", True)
        return list(cols)  # return a list of the dataframe columns

    def get_table(self, table):
        """Function used to import data from SQL Server to a Pandas DataFrame.

        Keyword arguments:
        table -- the name of the table we want to retrieve from SQL server
        """
        # we query for ALL data within the table we specified
        query = "SELECT * From [dbo].["+table+"]"

        # now send the query and connection parameters to 'read_sql' function
        data = read_sql(query, self.cnxn)

        # update the user
        print("{} table imported from {}. Type variable_name.head() to view, "
              "for example \"data.head()\".".format(table, self.database))
        return data

    def push_dataframe_dtypes(self, data, table="raw_data", batchsize=500,
                              overwrite=False, fast_upload=False):
        # if overwrite is true we auto remove any tables with same name
        if overwrite:
            # check for pre-existing table and delete if present
            self.drop(table)

        # convert pyodbc connection string into sqlalchemy friendly format
        connection_str = urllib.parse.quote_plus(self.connection_str)

        # sqlalchemy engine is required for insert here
        engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect'
                                          f'={connection_str}')

        method = None
        # if fast_upload chosen, set method to this
        if fast_upload:
            method = 'multi'

        # upload to SQL server
        data.to_sql(table, engine, chunksize=batchsize, method=method)

    def push_dataframe(self, data, table="raw_data", batchsize=500):
        """Function used to upload a Pandas DataFrame (data) to SQL Server.

        Keyword arguments:
        data -- the dataframe to be uploaded
        table -- the name of the new table in SQL (default "raw_data")
        batchsize -- the number of rows to upload to the new table within each
                     execution, recommend no more than 1000 (default 500)
        """
        # check for pre-existing table and delete if present
        self.drop(table)

        # create execution cursor
        cursor = self.cnxn.cursor()
        # activate fast execute
        cursor.fast_executemany = True

        # create create table statement
        query = "CREATE TABLE [" + table + "] (\n"

        # iterate through each column to be included in create table statement
        for i in range(len(list(data))):
            # add column (everything is varchar for now)
            query += "\t[{}] varchar(8000)".format(list(data)[i])
            # append correct connection/end statement code
            if i != len(list(data))-1:
                query += ",\n"
            else:
                query += "\n);"

        cursor.execute(query)  # execute the create table statement

        self.cnxn.commit()  # commit changes

        # append query to our SQL code logger
        self.query += ("\n\n-- create table\n" + query)

        start_time = datetime.now()  # start timer
        # tell user we have started the insert operation
        print("Insert started at {}.".format(start_time.strftime("%H:%M:%S")))
        # initialise the previous user update time
        last_check = start_time

        # insert the data in batches
        query = ("INSERT INTO [{}] ({})\n".format(table,
                                                  '['+'], ['  # get columns
                                                  .join(list(data)) + ']') +
                 "VALUES\n(?{})".format(", ?"*(len(list(data))-1)))
        # cursor docs: https://github.com/mkleehammer/pyodbc/wiki/Cursor

        # insert data into target table in batches of 'batchsize'
        for i in range(0, len(data), batchsize):
            if i+batchsize > len(data):
                batch = data[i: len(data)].values.tolist()
            else:
                batch = data[i: i+batchsize].values.tolist()

            # execute batch insert
            cursor.executemany(query, batch)
            # commit insert to SQL Server
            self.cnxn.commit()

            # so user can see progress being made
            if (datetime.now() - last_check).seconds > 10:

                # calculations for time print-out to user
                last_check = datetime.now()  # updating 'last print' time
                delta = datetime.now() - start_time  # time taken so far
                percentage = (i+batchsize) / len(data)  # percentage complete
                eta = start_time + (delta/percentage)  # eta

                # print above in readable format for user
                print("{:.1f}% complete\n".format(percentage*100) +
                      "Current Time: {}\n".format(datetime.now()
                                                  .strftime("%H:%M:%S")) +
                      "ETA: {}\n".format(eta.strftime("%H:%M:%S")))

        # let's see how long it took
        time_taken = str((datetime.now() - start_time).seconds)
        print("Insert completed in {} seconds.".format(time_taken))

        # append upload details to SQL code logger
        self.query += ("\n\n-- User uploaded "+table+" table\n"
                       "-- upload time: "+time_taken+" secs")

        # updating the user
        print("DataFrame uploaded as " + table +
              " to " + self.database + " on " + self.server + " server.")

    def push_raw(self, path, sheet=0, batchsize=500,
                 delimiter=",", verbose=False):
        """Function used to upload raw data from .xlsx/.csv file to SQL Server.
        Common formatting issues are taken care of, eg scientific notation or
        weird date formats, but this is minimal.

        Keyword arguments:
        path -- the full path to the target file, must include filename and
                file extension, example: "C:/Documents/datatape.xls"
        sheet -- excel files only, this selects the sheet to be imported, can
                 be either an integer representing the sheet index - counting
                 from 0, or a string of the sheet name
        batchsize -- the number of rows to upload to the new table within each
                     execution, recommend no more than 1000 (default 500)
        delimiter -- txt files only, this specifies the text file delimiter
                     (default ",")
        verbose -- Boolean value indicating whether to print extra detail to
                   the terminal or not (default False)
        """
        start_time = datetime.now()
        # get filename
        if sheet == 0:
            # if no sheetname included
            table = splitext(basename(path))[0]
        else:
            # if sheetname included
            table = splitext(basename(path))[0] + "." + str(sheet)
        # let user know what is happening
        print('Loading {}.'.format(table))
        if path[-4:] == '.csv':
            # if data is a csv
            try:
                data = read_csv(path, encoding="utf-8")  # try for utf-8
            except UnicodeDecodeError:
                # if utf-8 doesn't work, try latin-1
                data = read_csv(path, encoding="latin-1")
        elif path[-4:] in ['xlsx', 'xlsm', '.xls']:
            # checking if sheet is numeric and converting if so
            try:
                sheet = int(sheet)
            except ValueError:
                pass
            # if data is an xlsx file
            try:
                # try for utf-8 encoding first
                data = read_excel(path, encoding="utf-8", sheet_name=sheet)
            except UnicodeDecodeError:
                # now trying latin-1
                data = read_excel(path, encoding="latin-1", sheet_name=sheet)

        elif path[-4:] == '.txt':
            # if data is a txt file
            try:
                # try for utf-8
                data = read_csv(path, sep=delimiter, encoding="utf-8")
            except UnicodeDecodeError:
                # if utf-8 doesn't work, try latin-1
                data = read_csv(path, sep=delimiter, encoding="latin-1")
        else:
            raise KeyError("File extension not recognised. Please import "
                           "only .csv or Excel (xlsx, xlsm, xls) filetypes.")

        print("Imported '{}' in {} seconds.".format(table,
                                                    (datetime.now() -
                                                     start_time).seconds))

        # trimming leading/trailing whitespace from column names
        data.columns = data.columns.str.strip()

        # convert non-string columns to string (avoids errors, keeps it clean)
        data_types = data.dtypes.to_dict()
        for col in data_types:
            dtype = str(data_types[col])
            if dtype == 'datetime64[ns]':
                # for datetime columns -> string
                if verbose:
                    print("Converting {} (datetime) to string".format(col))
                # convert from datetime object to date string dd-mm-yyyy
                data[col] = data[col].apply(lambda x:
                                            x.strftime('%d-%m-%Y')
                                            .replace(' 00:00:00', '')
                                            if str(x) != 'NaT' else '')

            elif dtype in ('object', 'float64'):
                # for object/float columns -> string
                if verbose:
                    print("Converting {} (object/float) to string".format(col))
                data[col] = data[col].apply(lambda x:
                                            str(x) if str(x) != 'nan' else '')

        self.push_dataframe(data, table, batchsize)  # push data to SQL server
        del data  # delete data to free up RAM

        self.nullify(table)  # swap blank values for NULLs

        # let user know the total operation time
        print("Total time: {} seconds\n\n".format((datetime.now() -
                                                   start_time)
                                                  .seconds))

    def union(self, table_list, name="union", join="UNION"):
        """Pass a list of table names to union them all together. The join
        argument can be changed to alter between UNION/UNION ALL.

        Keyword arguments:
        table_list -- a list of table names, example: to union [dbo].[d1] and
                      [dbo].[d2], table_list = ["d1", "d2"]
        name -- the name of the table created by the union (default "union")
        join -- the union type, either "UNION" or "UNION ALL" (default "UNION")
        """
        # initialise the query
        query = "SELECT * INTO [dbo].["+name+"] FROM (\n"

        # build the SQL query
        query += f'\n{join}\n'.join(
                            [f'SELECT [{x}].* FROM [{x}]' for x in table_list]
                            )

        query += ") x"  # add end of query

        cursor = self.cnxn.cursor()  # create execution cursor

        cursor.fast_executemany = True  # activate fast execute

        # update user
        print("Executing {} operation for {} tables.".format(join,
                                                             len(table_list)))

        cursor.execute(query)  # execute

        self.cnxn.commit()  # commit union to SQL Server

        # append query to our SQL code logger
        self.query += ("\n\n-- union operation\n" + query)

        print("Union complete.\n")  # update user

    def drop(self, tables):
        """Pass a table or list of table names to drop.

        Keyword arguments:
        tables -- a single table name as a string, or a list of table names as
                  strings. For [dbo].[data] we would input "data"
        """
        # check if single or list
        if isinstance(tables, str):
            # if single string, convert to single item in list for for-loop
            tables = [tables]

        cursor = self.cnxn.cursor()  # create execution cursor

        for table in tables:
            # check for pre-existing table and delete if present
            try:
                # for the standard server (dbo)
                query = ("IF OBJECT_ID ('dbo.["+table+"]', 'U') IS NOT NULL "
                         "DROP TABLE dbo.["+table+"]")
                cursor.execute(query)  # execute

            except pyodbc.ProgrammingError as error:
                print("Warning:\n{}".format(error))  # print error as a warning
                # development server tablenames are dealt with differently if
                # not set up correctly, managers should correct when noticed,
                # but for now we need to pre-append user login (eg
                # 'uk\username.database')
                user = basename(expanduser('~'))
                print("Default schema not used, changing to uk\\"+user)
                query = ("IF OBJECT_ID ('[uk\\"+user+"].["+table+"]', 'U') "
                         "IS NOT NULL "
                         "DROP TABLE [uk\\"+user+"].["+table+"]")
                cursor.execute(query)  # execute
            # append query to our SQL code logger
            self.query += ("\n\n-- drop table\n" + query)

        self.cnxn.commit()  # commit drop(s) to SQL Server

        print("Tables dropped.")  # update user

    def manual(self, query, response=False, comment="manual query",
               verbose=False):
        """Enter a manual statement/query.

        Keyword arguments:
        query -- SQL query to run on SQL connection
        response -- Boolean value stating whether a response/table
                    should be returned (default False)
        comment -- string input that translates into a comment in the
                   self.query string (default "manual query")
        verbose -- Boolean value indicating whether to print extra detail to
                   the terminal or not (default True)

        Returns:
        if (response=True): a dataframe returned from the query sent
        if (response=False): a string to notify user manual query complete
        """
        cursor = self.cnxn.cursor()  # create execution cursor

        # append query to our SQL code logger
        self.query += ("\n\n-- "+str(comment)+"\n" + query)

        print("Executing query.")  # inform user
        if verbose:
            # print comment and query if user wants
            print(comment)
            print(query)

        if response:
            return read_sql(query, self.cnxn)  # get sql query
        try:
            cursor.execute(query)  # execute
        except pyodbc.ProgrammingError as error:
            if verbose:
                print("Warning:\n{}".format(error))  # print error as a warning
        self.cnxn.commit()  # commit query to SQL Server
        return "Query complete."

    def nullify(self, table, replace="", verbose=False):
        """Run through all columns in a table to convert a specific string
        value to NULL values.

        Keyword arguments:
        table -- the name of the target table in SQL, eg [dbo].[data] = "data"
        replace -- the cell values that should be replaced by a NULL value
                   (default "")
        verbose -- Boolean value indicating whether to print extra detail to
                   the terminal or not (default False)
        """
        col_list = self.get_cols(table)  # first lets get the column names
        # loop through each column and write to SQL table, swapping '' for NULL
        for col in col_list:
            if verbose:
                print("Nullifying ["+col+"] column.")  # update the user
            # create comment to input into code
            comment = "replacing '{}' with NULL in [{}]".format(replace, col)
            # use manual function to swap the replace string for NULLs
            res = self.manual("UPDATE [dbo].["+table+"]\n"
                              "SET ["+col+"] = NULLIF(["+col+"], '" +
                              replace+"')",
                              comment=comment,
                              verbose=verbose)
            if verbose:
                # if verbose, let user know query complete
                print(res)

    def extract(self, tables, target, batchsize=None):
        """Output a SQL table into Excel workbooks in a target directory.

        Keyword arguments:
        tables -- the table(s) to extract, can be a single table contained in
                  a string or a list of table names contained in strings
        target -- the target directory to save Excel file extracts to
        batchsize -- the number of rows to extract to a single Excel document,
                     if None then will extract to a single document, Excel
                     documents will be saved as table name appended with a
                     digit indicating the batch number
        """
        raise IOError('Function not complete.')
        # check data type of tables
        # check if single or list
        if isinstance(tables, str):
            # if single string, convert to single item in list for for-loop
            tables = [tables]

        # loop through tables in list to extract
        for table in tables:
            # if batchsize is an integer we create another loop to extract in
            # batches
            if type(batchsize) is int:
                # first we get length of table to extract
                length = self.manual(
                        f'select count(*) from [{table}]')[''].iloc[0]

                # create a temp version of this table with row indices, first
                # we must get a list of the column names (we use for row index)
                cols = self.get_cols(table)
                # we drop the temp table if exists
                self.manual("IF OBJECT_ID('tempdb..#temp_batch) IS NOT NULL "
                            "DROP TABLE #temp_batch")
                # now we create the temp table with a mssqlplus_row column
                self.manual("SELECT *, "
                            f"ROW_NUMBER() OVER (ORDER BY {cols}) "
                            "AS 'mssqlplus_row' INTO #temp_batch")
                # set batch indicator for filename
                batch_no = 1
                # we then loop upto this length
                for rows in range(0, length+batchsize, batchsize):
                    df = self.manual("SELECT * FROM #temp_batch "
                                     f"WHERE mssqlplus_row >= {rows} "
                                     f"AND mssqlplus_row < {rows+batchsize}",
                                     response=True)
                    # save dataframe to file
                    df.to_excel(target+'/'+table+str(batch_no)+'.xlsx',
                                index=False)

                    batch_no += 1  # increment batch counter
            else:
                # extract full table
                df = self.manual("SELECT * FROM [{table}]", response=True)
                # save dataframe to file
                df.to_excel(target+'/'+table+'.xlsx', index=False)

    def output_query(self, filename="query"):
        """Output the SQL query built by Python into a .txt file either locally
        or in a user specified directory.

        Keyword arguments:
        filename -- the filename of the query txt file. If only the file-name
                    is detected then it will be saved locally, if a filepath is
                    detected then it will be saved to that specific location
                    (default "query")
        """
        # if user is using default query name, append date and time to prevent
        # any overwriting
        if filename == "query":
            # get the current working directory + query + current date and time
            filename = (getcwd() + "/query_" +
                        datetime.now().strftime("%Y%m%d_%H-%M"))

        # open the filename given (or created above) ready for writing
        with open(r"{}.txt".format(filename), 'w') as f:
            # write the query to current working directory
            f.writelines(self.query)
