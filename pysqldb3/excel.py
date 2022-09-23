from unittest.mock import NonCallableMagicMock
import openpyxl as opxl
import pandas as pd
import os
import util
from . import Config
from . import pysqldb3 as pdb3


class DbConnectExcel:

    def pg_to_excel(self, pg, tbl_name, excel_path, schema='working'):
        # type: (pdb3.DbConnect, str, str, str) -> None
        """
        Migrates tables from a pgsql database to an MS Excel file.
        Each table will be saved as a seperate tab in Excel.
        :param pg: PostgreSQL DBConnect instance to export from
        :param tbl_name: Name of table to save as excel file
        :param excel_path: Excel filepath for output file
        :param schema: Schema to use, default working
        """
        pass

    def ms_to_excel(self, ms, tbl_name, excel_path, schema='dbo'):
        # type: (pdb3.DbConnect, str, str, str) -> None
        """
        Migrates tables from a MSSQL database to an MS Excel file.
        Each table will be saved as a seperate tab in Excel.
        :param ms: MS SQL Server DBConnect instance to export from
        :param tbl_name: Name of table to save as excel file
        :param excel_path: Excel filepath for output file
        :param schema: Schema to use, default dbo
        """
        pass
    
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
        pass
