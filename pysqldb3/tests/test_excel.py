from os import path
from ..excel import DbConnectExcel
import pytest
import pandas as pd
import numpy as np
import TestHelpers

class TestExcel():

    def test_df_to_excel(self):
        # Create dataframe with random ints and save it
        excel_path = TestHelpers.test_data_folder_path('testexcelsingle.xlsx')
        test_df = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df')
        DbConnectExcel.df_to_excel(test_df,filename='testexcelsingle')

        # Assert existance
        assert path.exists(excel_path)

        # Open excel_path as a new df
        test_df_2 = pd.read_excel(excel_path)

        # Assert dfs are equal
        assert test_df_2.equals(test_df)
    
    def test_df_to_excel_xls(self):
        # Create dataframe with random ints and save it
        excel_path = TestHelpers.test_data_folder_path('testexcelsingle.xls')
        test_df = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df')
        DbConnectExcel.df_to_excel(test_df,filename='testexcelsingle',as_xls=True)

        # Assert existance and xls format
        assert path.exists(excel_path)
        assert path.splitext()[1] == 'xls'

        # Open excel_path as a new df
        test_df_2 = pd.read_excel(excel_path)

        # Assert dfs are equal
        assert test_df_2.equals(test_df)
    
    def test_df_to_excel_custom_tab_name():
        # Create dataframe with random ints and save it
        excel_path = TestHelpers.test_data_folder_path('testexcelsinglenamedtab.xlsx')
        test_df = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df')

        # Assert existance
        assert path.exists(excel_path)

        # Open excel_path as a new df
        test_df_2 = pd.read_excel(excel_path)

        # Assert dfs are equal
        assert test_df_2.equals(test_df)
    
    def test_df_to_excel_multiple_tabs(self):
        excel_path = TestHelpers.test_data_folder_path('testexcelmulti.xlsx')

        # Create random dfs
        test_df1 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df1')
        test_df2 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df2')
        test_df3 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df3')

        # Save
        DbConnectExcel.df_to_excel()

        # Assert existence

        # Assert proper tabs

    def test_df_to_excel_multiple_tabs_custom_names(self):
        excel_path = TestHelpers.test_data_folder_path('testexcelmultinamedtabs.xlsx')

        # Create random dfs
        test_df1 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df1')
        test_df2 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df2')
        test_df3 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df3')

        # Save
        DbConnectExcel.df_to_excel_multi(df_list=[test_df1,test_df2,test_df3],filename='testexcelmultinamedtabs')
        
    def test_df_to_excel_multiple_tabs_diff_df_and_name_lengths(self):
        excel_path = TestHelpers.test_data_folder_path('testexcelmultinamedtabs.xlsx')

        # Create random dfs
        test_df1 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df1')
        test_df2 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df2')
        test_df3 = pd.DataFrame(np.random.random_integers(low=0,high=999999,size=(5,5)), name='pdb3_test_df3')

        # Try to save but assert ValueError
        with pytest.raises(ValueError):
            DbConnectExcel.df_to_excel_multi(df_list=[test_df1,test_df2,test_df3],filename='testexceldiffdfnamelength',
            tab_name_list=['tab1','tab2'])

    def test_pg_to_excel(self):
        pass

    def test_pg_to_excel_multiple_tabs(self):
        pass

    def test_pg_to_excel_multiple_tabs_custom_names(self):
        pass

    def test_ms_to_excel(self):
        pass

    def test_ms_to_excel_multiple_tabs(self):
        pass
    
    def test_ms_to_excel_multiple_tabs_custom_names(self):
        pass