import os
from configparser import ConfigParser
from osgeo import ogr, gdal
from . import helpers
from ogr_cmds import *
from .. import pysqldb3 as psdb3


config = ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "\\db_config.cfg")

# Set up test db's
pg_test_db = psdb3.DbConnect(type=config.get('PG_DB', 'TYPE'),
                       server=config.get('PG_DB', 'SERVER'),
                       database=config.get('PG_DB', 'DB_NAME'),
                       user=config.get('PG_DB', 'DB_USER'),
                       password=config.get('PG_DB', 'DB_PASSWORD'),
                       allow_temp_tables=True
                       )

ms_test_db = psdb3.DbConnect(type=config.get('SQL_DB', 'TYPE'),
                        server=config.get('SQL_DB', 'SERVER'),
                        database=config.get('SQL_DB', 'DB_NAME'),
                        user=config.get('SQL_DB', 'DB_USER'),
                        password=config.get('SQL_DB', 'DB_PASSWORD'),
                        allow_temp_tables=True)

test_table_name = f'__testing_ogr_query_to_shp_{pg_test_db.user}__'
test_shapefile_name_1 = 'LION_TEST_1.shp'
test_shapefile_name_2 = 'LION_TEST_2.shp'
ms_schema = 'risadmin'
pg_schema = 'working'

class TestOGRShapefileIO():

    @classmethod
    def setup(cls):
        helpers.set_up_shapefile()
        

    def test_ogr_shapefile_read_from_pg(self):
        query_result = read_shapefile_pg(shp_path=f'tests/test_data/{test_shapefile_name_1}', tbl_name=test_table_name, schema=pg_schema, srid=2263, capture_output=True)

    def test_ogr_shapefile_write_to_pg(self):
        query_result = write_shapefile_pg(shp_name=test_shapefile_name_1, tbl_name=test_table_name, export_path=f'tests/test_data/{test_shapefile_name_1}', srid=2263, capture_output=True)

    def test_ogr_shapefile_read_from_ms(self):
        query_result = read_shapefile_ms(shp_path=f'tests/test_data/{test_shapefile_name_2}', tbl_name=test_table_name, schema=ms_schema, srid=2263, capture_output=True)

    def test_ogr_shapefile_write_to_ms(self):
        query_result = write_shapefile_ms(shp_name=test_shapefile_name_2, tbl_name=test_table_name, export_path=f'tests/test_data/{test_shapefile_name_2}', srid=2263, capture_output=True)