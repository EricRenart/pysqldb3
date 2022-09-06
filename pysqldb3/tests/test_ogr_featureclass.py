import os
from configparser import ConfigParser
from osgeo import ogr, gdal
from . import helpers
from . import ogr_cmds
from . import pysqldb3 as psdb3


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

# ldap_sql = pysqldb.DbConnect(type='MS',
#                              database='CLION',
#                              server='DOTGISSQL01',
#                              ldap=True)

test_table_name = f'__testing_ogr_query_to_fc_{db.user}__'
test_gdb_name = 'test.gdb'
test_fc_name_1 = 'TEST_FC1'
test_fc_name_2 = 'TEST_FC2'
ms_schema = 'risadmin'
pg_schema = 'working'

class TestOGRFeatureclassIO:

    def test_ogr_featureclass_read_from_pg(self):
        result = ogr_cmds.read_feature_class_pg(fc_name=test_fc_name_1, geodatabase=test_gdb_name, tbl_name=test_table_name,
        schema=pg_schema, srid=2263, capture_output=True)

    def test_ogr_featureclass_read_from_ms(self):
        result = ogr_cmds.read_feature_class_ms(fc_name=test_fc_name_2, geodatabase=test_gdb_name,
        schema=ms_schema, srid=2263, capture_output=True)

    def test_ogr_featureclass_write_to_pg(self):
        pass

    def test_ogr_featureclass_write_to_ms(self):
        pass