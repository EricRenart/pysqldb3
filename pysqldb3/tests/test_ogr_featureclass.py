import os
from .. import ogr_cmds
from . import TestHelpers

class TestOGRFeatureclass():

    @classmethod
    def setup(cls):
        if os.path.exists('tests/test_data/lion/lion.gdb'):
            # Delete fc if it exists
            TestHelpers.clean_up_feature_class()
        TestHelpers.set_up_feature_class()

    def test_ogr_pg_to_featureclass(self):
        tblname = 'test_ogr_pg_to_featureclass_data_table'
        pg = TestHelpers.get_pg_dbc_instance()
        ogr_cmds.read_feature_class_pg(fc_name='lion', geodatabase='tests/test_data/lion/lion.gdb', tbl_name=tblname, capture_output=True)
        assert pg.table_exists(tblname)
        
        # cleanup
        pg.drop_table(table=tblname)

    def test_ogr_ms_to_featureclass(self):
        tblname = 'test_ogr_ms_to_featureclass_data_table'
        ms = TestHelpers.get_ms_dbc_instance()
        ogr_cmds.read_feature_class_ms(fc_name='lion', geodatabase='tests/test_data/lion/lion.gdb', tbl_name=tblname, capture_output=True)
        assert ms.table_exists(tblname)

        # cleanup
        ms.drop_table(table=tblname)