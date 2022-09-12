import os
from configparser import ConfigParser
from . import TestHelpers
from .. import ogr_cmds

class TestOGRShapefile():

    @classmethod
    def setup(cls):
        # Delete shapefile if exists
        if os.path.exists('test_data/test.shp'):
            TestHelpers.clean_up_shapefile()
        TestHelpers.set_up_shapefile()
    
    def test_ogr_shapefile_read_to_pg(self):
        pg = TestHelpers.get_pg_dbc_instance()
        table_name = 'test_ogr_shp_to_pg_table'
        ogr_cmds.read_shapefile_pg(shp_name='test_data/test.shp', tbl_name=table_name, capture_output=True)
        assert len(pg.get_table_columns(table=table_name)) > 1

        # clean up
        TestHelpers.clean_up_shapefile()
        pg.drop_table(schema='working', table=table_name)

    def test_ogr_shapefile_write_pg_to_shp(self):
        table_name = 'test_ogr_pg_to_shp_table'
        ogr_cmds.write_shapefile_pg(shp_name='test_data/test_pg.shp', tbl_name=table_name, capture_output=True)
        assert os.path.exists('test_data/test_pg.shp')
        
        # clean up
        TestHelpers.clean_up_shapefile()

    def test_ogr_shapefile_read_to_ms(self):
        ms = TestHelpers.get_ms_dbc_instance()
        table_name = 'test_ogr_shp_to_ms_table'
        ogr_cmds.read_shapefile_ms(shp_path='test_data/test.shp', tbl_name=table_name, capture_output=True)
        assert len(ms.get_table_columns(table=table_name)) > 1

        # clean up
        TestHelpers.clean_up_shapefile()
        ms.drop_table(schema='working', table=table_name)

    def test_ogr_shapefile_write_to_ms(self):
        table_name = 'test_ogr_ms_to_shp_table'
        ogr_cmds.write_shapefile_ms(shp_name='test_data/test_ms.shp', tbl_name=table_name, capture_output=True)
        assert os.path.exists('test_data/test_ms.shp')

        # Clean up
        TestHelpers.clean_up_shapefile()