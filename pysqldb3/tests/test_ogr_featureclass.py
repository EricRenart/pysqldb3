import os
import pytest
from .. import ogr_cmds
from . import TestHelpers

class TestOGRFeatureclass():

    @classmethod
    def setup(cls):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__)), 'lion.gdb'):
            # Delete fc if it exists
            TestHelpers.clean_up_feature_class()
        TestHelpers.set_up_feature_class()

    @pytest.mark.ogr
    def test_ogr_pg_to_featureclass(self):
        pg = TestHelpers.get_pg_dbc_instance()
        tblname = f'test_ogr_pg_to_featureclass_data_table_{pg.user}'
        gdb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lion.gdb')
        ogr_cmds.read_featureclass_pg(fc_name='lion', geodatabase=gdb_dir, tbl_name=tblname)
        assert pg.table_exists(tblname)
        
        # cleanup
        pg.drop_table(table=tblname)

    @pytest.mark.ogr
    def test_ogr_ms_to_featureclass(self):
        ms = TestHelpers.get_ms_dbc_instance()
        tblname = f'test_ogr_ms_to_featureclass_data_table_{ms.user}'
        gdb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lion.gdb')
        ogr_cmds.read_featureclass_ms(fc_name='lion', geodatabase=gdb_dir, tbl_name=tblname)
        assert ms.table_exists(tblname)

        # cleanup
        ms.drop_table(table=tblname)