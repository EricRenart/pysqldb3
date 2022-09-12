import os
from .. import ogr_cmds
from . import helpers

class TestOGRFeatureclass():

    @classmethod
    def setup(cls):
        if os.path.exists('tests/test_data/lion/lion.gdb'):
            helpers.clean_up_feature_class()
        helpers.set_up_feature_class()

    def test_ogr_pg_to_featureclass(self):
        tblname = 'test_ogr_pg_to_featureclass_data_table'
        pg = helpers.get_pg_dbc_instance()
        ogr_cmds.read_feature_class_pg(fc_name='lion', geodatabase='tests/test_data/lion/lion.gdb', tbl_name=tblname, capture_output=True)
        assert pg.table_exists(tblname)

    def test_ogr_ms_to_featureclass(self):
        tblname = 'test_ogr_ms_to_featureclass_data_table'
        ms = helpers.get_ms_dbc_instance()
        ogr_cmds.read_feature_class_ms(fc_name='lion', geodatabase='tests/test_data/lion/lion.gdb', tbl_name=tblname, capture_output=True)
        assert ms.table_exists(tblname)