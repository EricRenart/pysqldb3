import os
from .. import ogr_cmds
from . import TestHelpers

# Path to test gdb
gdb_path = "\\lion\\lion.gdb"

class TestOGRFeatureclass():

    @classmethod
    def setup(cls):
        if os.path.exists(gdb_path):
            # Delete fc if it exists
            TestHelpers.clean_up_feature_class()
        TestHelpers.set_up_feature_class()

    def test_ogr_pg_to_featureclass(self):
        tblname = 'test_ogr_pg_to_featureclass_data_table'
        pg = TestHelpers.get_pg_dbc_instance()
        gdb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data' + gdb_path
        ogr_cmds.read_featureclass_pg(fc_name='lion', geodatabase=gdb_dir, tbl_name=tblname)
        assert pg.table_exists(tblname)
        
        # cleanup
        pg.drop_table(table=tblname)

    def test_ogr_ms_to_featureclass(self):
        tblname = 'test_ogr_ms_to_featureclass_data_table'
        ms = TestHelpers.get_ms_dbc_instance()
        gdb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data' + gdb_path
        ogr_cmds.read_featureclass_ms(fc_name='lion', geodatabase=gdb_dir, tbl_name=tblname)
        assert ms.table_exists(tblname)

        # cleanup
        ms.drop_table(table=tblname)