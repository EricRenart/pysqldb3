import os
from configparser import ConfigParser
from . import TestHelpers
from .. import ogr_cmds

shp_path = "test_data\\test.shp"
shp_path_pg = "test_data\\test_pg.shp"
shp_path_ms = "test_data\\test_ms.shp"

class TestOGRShapefile():

    @classmethod
    def setup(cls):
        # Delete shapefiles if they exist
        # not the most elegant way to check but it works
        if os.path.exists(shp_path) or os.path.exists(shp_path_pg) or os.path.exists(shp_path_ms):
            TestHelpers.clean_up_shapefile()
        TestHelpers.set_up_shapefile()
    
    def test_ogr_shapefile_read_to_pg(self):
        pg = TestHelpers.get_pg_dbc_instance()
        table_name = 'test_ogr_shp_to_pg_table'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data' + shp_path
        ogr_cmds.read_shapefile_pg(shp_name=shp_dir, tbl_name=table_name, capture_output=True)
        assert len(pg.get_table_columns(table=table_name)) > 1

        # clean up
        TestHelpers.clean_up_shapefile()
        pg.drop_table(schema='working', table=table_name)

    def test_ogr_shapefile_write_pg_to_shp(self):
        table_name = 'test_ogr_pg_to_shp_table'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data' + shp_path
        ogr_cmds.write_shapefile_pg(shp_name=shp_dir, tbl_name=table_name, capture_output=True)
        assert os.path.exists(shp_path_pg)
        
        # clean up
        TestHelpers.clean_up_shapefile()

    def test_ogr_shapefile_read_to_ms(self):
        ms = TestHelpers.get_ms_dbc_instance()
        table_name = 'test_ogr_shp_to_ms_table'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data' + shp_path
        ogr_cmds.read_shapefile_ms(shp_path=shp_dir, tbl_name=table_name, capture_output=True)
        assert len(ms.get_table_columns(table=table_name)) > 1

        # clean up
        TestHelpers.clean_up_shapefile()
        ms.drop_table(schema='dbo', table=table_name)

    def test_ogr_shapefile_write_ms_to_shp(self):
        table_name = 'test_ogr_ms_to_shp_table'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data' + shp_path
        ogr_cmds.write_shapefile_ms(shp_name=shp_dir, tbl_name=table_name, capture_output=True)
        assert os.path.exists(shp_path_ms)

        # Clean up
        TestHelpers.clean_up_shapefile()