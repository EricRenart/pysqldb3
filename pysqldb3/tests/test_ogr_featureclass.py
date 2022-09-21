import os
import pytest
from .. import ogr_cmds
from . import TestHelpers

LION_GDB_PATH = 'lion/lion.gdb'

class TestOGRFeatureclass():

    @classmethod
    def setup(cls):
        lion_loc = TestHelpers.test_data_folder_path(LION_GDB_PATH)
        if lion_loc is None:
            # Delete and re-download lion.gdb
            TestHelpers.clean_up_feature_class()
            TestHelpers.set_up_feature_class()

    @pytest.mark.ogr
    def test_ogr_pg_to_featureclass(self):
        pg = TestHelpers.get_pg_dbc_instance()
        tblname = f'test_ogr_pg_to_featureclass_data_table_{pg.user}'
        ogr_cmds.read_featureclass_pg(fc_name='lion', geodatabase=TestHelpers.test_data_folder_path(LION_GDB_PATH), tbl_name=tblname)
        assert pg.table_exists(tblname)
        
        # cleanup
        TestHelpers.drop_all_tables_pg()

    @pytest.mark.ogr
    def test_ogr_ms_to_featureclass(self):
        ms = TestHelpers.get_ms_dbc_instance()
        tblname = f'test_ogr_ms_to_featureclass_data_table_{ms.user}'
        ogr_cmds.read_featureclass_ms(fc_name='lion', geodatabase=TestHelpers.test_data_folder_path(LION_GDB_PATH), tbl_name=tblname)
        assert ms.table_exists(tblname)

        # cleanup
        TestHelpers.drop_all_tables_ms()