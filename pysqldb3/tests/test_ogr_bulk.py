import os
import pytest
import pandas as pd
from .. import ogr_cmds
from . import TestHelpers

# Path to bulk test data
bulk_data_path = os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\bulk\\"

# Required CSV files in tests/test_data/bulk/ for testing
reqd_files = [os.path.abspath(bulk_data_path+'test1.csv'), os.path.abspath(bulk_data_path+'test2.csv'), 
os.path.abspath(bulk_data_path+'test3.csv'), os.path.abspath(bulk_data_path+'test4.csv')]

class TestOGRBulkData():

    @pytest.mark.ogr
    def test_ogr_bulk_to_pg(self):
        pg = TestHelpers.get_pg_dbc_instance()
        pg.connect()

        # assert correct csvs in dir
        filenames = os.listdir(bulk_data_path)
        #assert filenames.__eq__(reqd_files)

        # read in csvs
        tbl_name = f"ogr_pg_bulk_file_to_table_{pg.user}"
        ogr_cmds.pg_bulk_file_to_table(filenames, dest_table=tbl_name)

        # Assert data in table
        assert pg.table_exists(tbl_name)
        assert len(pg.dfquery(f"SELECT TABLE {tbl_name}")) == 20

    @pytest.mark.ogr
    def test_ogr_bulk_to_ms(self):
        ms = TestHelpers.get_ms_dbc_instance()
        ms.connect()

        # assert correct csvs in dir
        filenames = os.listdir(bulk_data_path)
        #assert filenames.__eq__(reqd_files)

        # read in csvs
        tbl_name = f"ogr_ms_bulk_file_to_table_{ms.user}"
        ogr_cmds.ms_bulk_file_to_table(filenames, dest_table=tbl_name)

        # Assert data in table
        assert ms.table_exists(tbl_name)
        assert len(ms.dfquery(f"SELECT TABLE {tbl_name}")) == 20