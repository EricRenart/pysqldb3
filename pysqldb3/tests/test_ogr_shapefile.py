import os
import pytest
from configparser import ConfigParser
from . import TestHelpers
from .. import ogr_cmds

shp_path = "test_data/test.shp"
shp_path_pg = "test_data/test_pg.shp"
shp_path_ms = "test_data/test_ms.shp"

class TestOGRShapefile():

    @classmethod
    def setup(cls):
        pass
    
    def cleanup_test_shapefiles(self):
        # Delete shapefiles if they exist
        # not the most elegant way to check but it works
        if os.path.exists(os.path.join(os.path.abspath(__file__), shp_path)):
            TestHelpers.clean_up_shapefile('test')
        if os.path.exists(os.path.join(os.path.abspath(__file__), shp_path_pg)):
            TestHelpers.clean_up_shapefile('test_pg')
        if os.path.exists(os.path.join(os.path.abspath(__file__), shp_path_ms)):
            TestHelpers.clean_up_shapefile('test_ms')
    
    @pytest.mark.ogr
    def test_ogr_shapefile_read_to_pg(self):
        pg = TestHelpers.get_pg_dbc_instance()
        table_name = f'test_ogr_shp_to_pg_table_{pg.user}'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__),shp_path))
        ogr_cmds.read_shapefile_pg(shp_path=shp_dir, tbl_name=table_name, capture_output=True)
        assert len(pg.get_table_columns(table=table_name)) > 1

        # clean up
        TestHelpers.drop_all_tables_pg()

    @pytest.mark.ogr
    def test_ogr_shapefile_write_pg_to_shp(self):
        pg = TestHelpers.get_pg_dbc_instance()
        table_name = f'test_ogr_pg_to_shp_table_{pg.user}'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),shp_path)
        ogr_cmds.write_shapefile_pg(shp_path=shp_dir, tbl_name=table_name, capture_output=True)
        assert os.path.exists(shp_path_pg)
        
        # clean up
        TestHelpers.drop_all_tables_pg()

    @pytest.mark.ogr
    def test_ogr_shapefile_read_to_ms(self):
        ms = TestHelpers.get_ms_dbc_instance()
        table_name = f'test_ogr_shp_to_ms_table_{ms.user}'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), shp_path)
        ogr_cmds.read_shapefile_ms(shp_path=shp_dir, tbl_name=table_name, capture_output=True)
        assert len(ms.get_table_columns(table=table_name)) > 1

        # clean up
        TestHelpers.drop_all_tables_ms()

    @pytest.mark.ogr
    def test_ogr_shapefile_write_ms_to_shp(self):
        ms = TestHelpers.get_ms_dbc_instance()
        table_name = f'test_ogr_ms_to_shp_table_{ms.user}'
        shp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), shp_path)
        ogr_cmds.write_shapefile_ms(shp_path=shp_dir, tbl_name=table_name, capture_output=True)
        assert os.path.exists(shp_path_ms)

        # Clean up
        TestHelpers.drop_all_tables_ms()