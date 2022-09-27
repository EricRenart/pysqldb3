import openpyxl as opxl
import pandas as pd
import os
from . import util
from . import Config
from . import pysqldb3 as pdb3


class DbConnectExcel:

    def pg_to_excel(self, pg, tbl_names, excel_path, query=None, tab_name_list=None, schema='working', as_xls=False):
        # type: (pdb3.DbConnect, list(str), str, str, list(str), str, bool) -> None
        """
        Migrates tables from a pgsql database to an MS Excel file.
        Each table will be saved as a seperate tab in Excel.
        :param pg: PostgreSQL DBConnect instance to export from
        :param tbl_names: Name of table to save as excel file
        :param excel_path: Excel filepath for output file
        :param query: SQL Query to execute. If None, all rows will be returned
        :param tab_name_list: List of tab names for pgsql tables. If None, defaults to pgsql table names.
        :param schema: Schema to use, default working
        :param as_xls: Whether to save as an Excel 97 file (xls) rather than xlsx. Default false.
        """

        # Connect to db
        pg.connect()

        # dfquery each table name and build a list of result dfs
        dfs = []
        for tn in tbl_names:
            dfqry = f"SELECT FROM {schema}.{tn}"
            if query:
                dfqry = f"""{dfqry} WHERE (
                    {query}
                    )"""
            res = pg.dfquery(dfqry)
            dfs.append(res)
        
        # save as excel file
        fp = os.path.splitext(excel_path)[0]
        if len(dfs) > 1:
            self.df_to_excel_multi(dfs, filename=fp, tab_name_list=tab_name_list, as_xls=as_xls)
        else:
            # only one tabname in list so this is ok
            self.df_to_excel(dfs[0], filename=fp, tab_name=tab_name_list[0], as_xls=as_xls)


    def ms_to_excel(self, ms, tbl_names, excel_path, query=None, tab_name_list=None, schema='dbo', as_xls=False):
        # type: (pdb3.DbConnect, list(str), str, str, list(str), str, bool) -> None
        """
        Migrates tables from a MSSQL database to an MS Excel file.
        Each table will be saved as a seperate tab in Excel.
        :param ms: MS SQL Server DBConnect instance to export from
        :param tbl_names: Name of table to save as excel file
        :param excel_path: Excel filepath for output file
        :param query: SQL Query to execute. If None, all rows will be returned
        :param tab_name_list: List of tab names for pgsql tables. If None, defaults to pgsql table names.
        :param schema: Schema to use, default working
        :param as_xls: Whether to save as an Excel 97 file (xls) rather than xlsx. Default false.
        """
        
        # connect to db
        ms.connect()

        # dfquery each table name and build a list of result dfs
        dfs = []
        for tn in tbl_names:
            dfqry = f"SELECT FROM {schema}.{tn}"
            if query:
                dfqry = f"""{dfqry} WHERE (
                    {query}
                    )"""
            res = ms.dfquery(dfqry)
            dfs.append(res)
        
        # save as excel file
        fp = os.path.splitext(excel_path)[0]
        if len(dfs) > 1:
            self.df_to_excel_multi(dfs, filename=fp, tab_name_list=tab_name_list, as_xls=as_xls)
        else:
            # only one tabname in list so this is ok
            self.df_to_excel(dfs[0], filename=fp, tab_name=tab_name_list[0], as_xls=as_xls)
    
    def df_to_excel(self, df, filename, tab_name=None, as_xls=False):
        # type: (pd.DataFrame, str, str, bool) -> None
        """
        Saves a Pandas DataFrame as an excel file at the specified path.
        :param df: Dataframe to save as excel
        :param excel_filename: Filename for excel file (omitting .xls/.xlsx)
        :param tab_name: Name of sheet to save in Excel file. Defaults to df name.
        :param as_xls: Whether to save the df as an Excel 97 file (xls) rather than xlsx
        """
        file_with_ext = util.output_path(f"{filename}.xls")
        if not as_xls:
            file_with_ext = f"{file_with_ext}x"
        
        # Save
        df.to_excel(file_with_ext, sheet_name=df.Name)
    
    def df_to_excel_multi(self, df_list, filename, tab_name_list=None, as_xls=False):
        """
        Saves a list of Pandas DataFrames to an Excel file. Each df is saved as its own tab.
        :param df_list: List of DataFrames to save
        :param filename: Filename for excel file (omitting .xls/.xlsx)
        :param tab_name_list: List of tab names for dataframes. Length must be equal to number of dataframes.
        If it isn't, ValueError is raised.
        :param as_xls: Whether to save the df as an Excel 97 file (xls) rather than xlsx
        """
        if not as_xls:
            filename = f"{filename}x"
        if len(df_list) != len(tab_name_list) and tab_name_list != None:
            raise ValueError('Length of list of dataframes and list of tab names must be equal')
        
        # Save
        with pd.ExcelWriter(util.output_path(filename), if_sheet_exists='replace') as writer:
            for i, df in enumerate(df_list):
                df.to_excel(writer, sheet_name=tab_name_list[i])