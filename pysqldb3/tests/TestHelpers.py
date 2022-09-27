import random
import os
import subprocess
import pandas as pd
from .. import pysqldb3 as psdb3
import shutil
import requests
import logging
import zipfile
from .. import Config
from configparser import ConfigParser
from xlrd import open_workbook
from xlutils.copy import copy


DIR = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '\\test_data'
pg_test_schema = 'testing'
ms_test_schema = 'testing'

def set_up_test_csv():
    data = {'id': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
            'living space (sq ft)': {0: 2222, 1: 1628, 2: 3824, 3: 1137, 4: 3560},
            'beds': {0: 3, 1: 3, 2: 5, 3: 3, 4: 6},
            'baths': {0: 3, 1: 2.5, 2: 4.0, 3: 2.0, 4: 4.0},
            'zip': {0: 32312, 1: 32308, 2: 32312, 3: 32309, 4: 32309},
            'year': {0: 1981, 1: 2009, 2: 1954, 3: 1993, 4: 1973},
            'list price': {0: 250000, 1: 185000, 2: 399000, 3: 150000, 4: 315000},
            'neighborhood': {0: 'Corona', 1: 'Kensington', 2: 'Morris Heights', 3: 'Bayside', 4: 'Inwood'},
            'sale date': {0: '1/1/2015', 1: '2/25/2012', 2: '7/9/2018', 3: '12/2/2021', 4: '11/13/1995'}}
    df = pd.DataFrame(data)
    df.to_csv(os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\test.csv", index=False)
    df.to_csv(os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\test2.csv", index=False, sep='|')
    df.to_csv(os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\test3.csv", index=False, header=False)

    data['neighborhood'][0] = data['neighborhood'][0] * 500
    df.to_csv(os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\varchar.csv", index=False, header=False)


def set_up_test_table_sql(sql, schema='dbo'):
    """
    Creates one test table for testing

    Uses random to make randomly generated inputs.
    """
    table_name = f'sql_test_table_{sql.user}'

    if sql.table_exists(table=table_name, schema=schema):
        return

    sql.query(f"""
    CREATE TABLE {schema}.{table_name} (test_col1 int, test_col2 int, geom geometry);
    INSERT INTO {schema}.{table_name} VALUES(1, 2, geometry::Point(985831.79200444, 203371.60461367, 2263));
    INSERT INTO {schema}.{table_name} VALUES(3, 4, geometry::Point(985831.79200444, 203371.60461367, 2263));
    """)

def set_up_simple_test_table_sql(sql, table_name, schema='dbo'):
    
    # Append db username to test table name
    table_name = f'{table_name}_{sql.user}'

    # Query to create table. No fancy randomness here - just two int columns with placeholder values
    sql.query(f"""
         CREATE TABLE {schema}.{table_name} (test_col1 int, test_col2 int);
         INSERT INTO {schema}.{table_name} (test_col1, test_col2) VALUES (1, 2);
         INSERT INTO {schema}.{table_name} (test_col1, test_col2) VALUES (3, 4);
         """)

def clean_up_test_table_sql(sql, schema='dbo'):
    table_name = 'sql_test_table_{}'.format(sql.user)
    sql.drop_table(table=table_name, schema=schema)

def clean_up_simple_test_table_sql(sql, table_name, schema='dbo'):
    # Append db username to test table name
    table_name = f'{table_name}_{sql.user}'

    # drop table
    sql.drop_table(table=table_name, schema=schema)

def set_up_simple_test_table_pg(db, table_name, schema='working'):
    # Append db username to test table name
    table_name = f'{table_name}_{db.user}'

    # Query to create table. No fancy randomness here - just two int columns with placeholder values
    db.query(f"""
         CREATE TABLE {schema}.{table_name} (test_col1 int, test_col2 int);
         INSERT INTO {schema}.{table_name} (test_col1, test_col2) VALUES (1, 2);
         INSERT INTO {schema}.{table_name} (test_col1, test_col2) VALUES (3, 4);
         """)

def clean_up_simple_test_table_pg(db, table_name, schema='working'):
    # Drop table
    db.drop_table(table=f'{table_name}_{db.user}', schema=schema)

def set_up_test_table_pg(db, schema='working'):
    """
    Creates one test table for testing

    Uses random to make randomly generated inputs.
    """
    table_name = f'pg_test_table_{db.user}'

    if db.table_exists(table=table_name, schema=schema):
        return

    db.query(f"""
    CREATE TABLE {schema}.{table_name}(
        id int, 
        test_col1 int, 
        test_col2 int, 
        geom geometry);
    """)
    for i in range(0, 1000):
        c1 = random.randint(0, 10000)
        c2 = random.randint(0, 10000)

        dec_lat = random.random() / 100
        dec_lon = random.random() / 100

        lat = 40.7 + dec_lat
        lon = -74 + dec_lon

        db.query(f"""
        INSERT INTO {schema}.{table_name} VALUES
        ({i}, {c1}, {c2}, ST_SetSRID(ST_MakePoint({lat}, {lon}), 4326))
        """)


def clean_up_test_table_pg(db):
    # Drop test table
    db.drop_table(table=f'pg_test_table_{db.user}', schema='working')


def set_up_two_test_tables_pg(db):
    """
    Creates two test tables for testing

    Uses random to make randomly generated inputs.
    """
    table_name = f'pg_test_table_{db.user}'
    table_name2 = f'pg_test_table_{db.user}_2'
    if db.table_exists(table=table_name, schema='working') and \
            db.table_exists(table=table_name2, schema='working'):
        return
    else:
        db.drop_table(table=table_name, schema='working')
        db.drop_table(table=table_name2, schema='working')

    db.query(f"""
    CREATE TABLE working.{table_name} (id int, test_col1 int, test_col2 int, geom geometry);
    """)

    db.query(f"""
    CREATE TABLE working.{table_name2} (id int, test_col1 int, test_col2 int, geom geometry);
    """)

    for i in range(0, 10000):
        c1 = random.randint(0, 10000)
        c2 = random.randint(0, 10000)

        dec_lat = random.random() / 100
        dec_lon = random.random() / 100

        lat = 40.7 + dec_lat
        lon = -74 + dec_lon

        dec_lat2 = random.random() / 100
        dec_lon2 = random.random() / 100

        lat2 = 40.7 + dec_lat2
        lon2 = -74 + dec_lon2

        db.query(f"""
        INSERT INTO working.{table_name} VALUES
        ({i}, {c1}, {c2}, ST_SetSRID(ST_MakePoint({lat}, {lon}), 4326))
        """)

        db.query(f"""
        INSERT INTO working.{table_name2} VALUES
        ({i}, {c1}, {c2}, ST_SetSRID(ST_MakePoint({lat2}, {lon2}), 4326))
        """)


def clean_up_two_test_tables_pg(db):
    table_name = f'pg_test_table_{db.user}'
    table_name2 = f'pg_test_table_{db.user}_2'
    db.drop_table(table=table_name, schema='working')
    db.drop_table(table=table_name2, schema='working')


def set_up_feature_class():
    """
    Builds file gdb with a feature class with sample data
    :return:
    """
    zip_path = test_data_folder_path('nyclion_22b.zip')
    if not os.path.isfile(zip_path):
        download_url = r'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyclion_22b.zip' # Updated LION link for 22b
        r = requests.get(download_url)
        with open(zip_path, 'wb') as f:
            f.write(r.content)
    gdb = os.path.join(os.path.dirname(zip_path), 'lion/lion.gdb')
    if not os.path.isfile(gdb):
        print(f"Extracting sample data {os.path.dirname(zip_path)}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(zip_path))

def set_up_small_feature_class():
    """
    Selects a subset of LION corresponding to the Bayside neighborhood of Queens, and saves it as a new feature in lion.gdb using ogr.
    This is to speed up testing with the mssql database
    """
    if not os.path.exists(test_data_folder_path('lion/lion.gdb')):
        logging.info('Lion.gdb does not exist in tests/test_data, retrieving it now.')
        set_up_feature_class()
    ogr_cmd = ['ogr2ogr','-config','GDAL_DATA',Config.get_gdal_data_path(),'-f','OpenFileGDB',
    test_data_folder_path('lion/lion.gdb'),test_data_folder_path('lion/lion.gdb'),'lion','-a_srs',
    'EPSG:2263','-sql','SELECT FROM lion WHERE "LZip" == "11361" OR "LZip" == "11364"','-nln','lion_bayside','-progress']
    subprocess.call(ogr_cmd)
    logging.info("Successfully saved new fc named 'lion_bayside' in lion.gdb")

def clean_up_feature_class():
    zip_path = test_data_folder_path('nyclion_22b.zip')
    gdb_path = test_data_folder_path('lion/lion.gdb')
    print ('Deleting any existing gdb')
    shutil.rmtree(gdb_path)

def clean_up_small_feature_class():
    """
    Deletes lion_bayside FC in lion.gdb
    """
    pass

# def set_up_fc_and_shapefile():
#     """
#     Builds file gdb with a feature class with sample data
#     Builds a shapefile for import
#     :return:
#     """
#     fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')
#     set_up_feature_class()
#
#     print 'Deleting any existing shp'
#     shp = 'test_feature_class.shp'
#     Delete_management(os.path.join(fldr, shp))
#
#     print 'Building shapefile'
#     FeatureClassToShapefile_conversion(["test_feature_class"], fldr)
#
#
# def clean_up_fc_and_shapefile():
#     fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')
#     gdb = "fGDB.gdb"
#     shp = 'test_feature_class.shp'
#
#     Delete_management(os.path.join(fldr, gdb))
#     Delete_management(os.path.join(fldr, shp))
#     print 'Deleted ESRI sample files'
#
#

def test_folder_path(pathstr=None):
    # type: (str) -> str
    """
    Gets absolute path of specified file in test folder.
    Raises FileNotFoundError if path doesn't exist.
    """
    if pathstr is None:
        return os.path.dirname(os.path.abspath(__file__))
    else:
        fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), pathstr)
        if not os.path.exists(fp):
            raise FileNotFoundError(f'File {pathstr} not found in tests directory. Please check for its existence.')
        return fp

def test_data_folder_path(pathstr=None):
    # type: (str) -> str
    """
    Gets absolute path of specified file in test data folder (tests/test_data).
    If no argument is specified, returns absolute path of test data folder
    Raises FileNotFoundError if path doesn't exist.
    """
    if pathstr is None:
        return test_folder_path('test_data')
    else:
        return os.path.join(test_folder_path('test_data'), pathstr)

def set_up_shapefile():
    data = {
        'gid': {0: 1, 1: 2},
        'WKT': {0: 'POINT(-73.88782477721676 40.75343453961836)', 1: 'POINT(-73.88747073046778 40.75149365677327)'},
        'some_value': {0: 'test1', 1: 'test2'}
    }
    df = pd.DataFrame(data)
    fle = test_data_folder_path('sample.csv')
    df.to_csv(fle, index=False)
    pth = test_data_folder_path('test.shp')

    subprocess.call(['ogr2ogr','-f','ESRI Shapefile',pth,'-dialect','sqlite','-sql',
    f"SELECT (gid, GeomFromText(WKT,4326), some_value) FROM sample",{fle}])
    print ('Sample shapefile ready...')


def clean_up_shapefile(filename='test'):
    """
    Deletes the shapefile the test suite downloads during testing.
    :param filename: The filename of the shapefile to delete (not including extension)
    """
    print('Deleting any existing shp')
    fldr = test_data_folder_path()
    for ext in ('shp', 'dbf', 'shx'):
        os.remove(f'{fldr}\\{filename}.{ext}')
    
    # Delete_management(os.path.join(fldr, shp))


def set_up_schema(db, ms_schema='dbo', pg_schema='working'):
    if db.type == 'MS':
        db.query(f"""
            IF NOT EXISTS (
                SELECT  schema_name
                FROM    information_schema.schemata
                WHERE   schema_name = '{ms_schema}' 
            ) 
             
            BEGIN
            EXEC sp_executesql N'CREATE SCHEMA {ms_schema}'
            END
        """)
    if db.type == 'PG':
        db.query(f"""
            CREATE SCHEMA IF NOT EXISTS {pg_schema};
        """)


def clean_up_schema(db, schema):
    if db.type == 'PG':
        c = ' CASCADE'
    else:
        c = ''
    db.query(f"DROP SCHEMA IF EXISTS {schema}{c};")

def clean_up_shp(file_path):
    for ext in ('.shp', '.dbf', '.shx', '.prj'):
        clean_up_file(file_path.replace('.shp', ext))

def clean_up_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"File removed: {os.path.basename(file_path)}")

def set_up_xls():
    xls_file1 = os.path.join(DIR, 'test_xls.xls')
    if os.path.isfile(xls_file1):
        clean_up_file(xls_file1)

    test_df1 = pd.DataFrame({'a': {0: 1, 1: 2}, 'b': {0: 3, 1: 4}, 'Unnamed: 0': {0: 0, 1: 1}})
    test_df1.to_excel(os.path.join(DIR, 'test_xls.xls'))
    print(f'File created: {os.path.basename(xls_file1)}')

    xls_file2 = os.path.join(DIR, 'test_xls_with_sheet.xls')
    if os.path.isfile(xls_file2):
        clean_up_file(xls_file2)

    test_df2 = pd.DataFrame({'a': {0: 1, 1: 2}, 'b': {0: 3, 1: 4}, 'Unnamed: 0': {0: 0, 1: 1}})

    test_df2.to_excel(os.path.join(DIR, 'test_xls_with_sheet.xls'), sheet_name='AnotherSheet')
    w = copy(open_workbook(xls_file2))
    Sheet2 = w.add_sheet('Sheet2')
    col, row = 0, 0
    Sheet2.write(row, col, '')
    row += 1
    for i in range(len(test_df2)):
        Sheet2.write(row, col, i)
        row += 1
    col, row = 1, 0
    for c in test_df2.columns:
        Sheet2.write(row, col, c)
        row += 1
        for r in test_df2[c]:
            Sheet2.write(row, col, r)
            row += 1
        col += 1
        row = 0
    w.save(xls_file2)
    print(f'File created: {xls_file2}')

def get_pg_dbc_instance(section_prefix=None, temp_tables=True):
        """
        Gets a new PostgreSQL DbConnect, reading parameters from config
        """
        config = ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + "\\db_config.cfg")
        sec_str = 'PG_DB'
        if section_prefix is not None:
            sec_str = f'{section_prefix}_{sec_str}'
        return psdb3.DbConnect(type='PG',
                    server=config.get(sec_str, 'SERVER'),
                    database=config.get(sec_str, 'DB_NAME'),
                    user=config.get(sec_str, 'DB_USER'),
                    password=config.get(sec_str, 'DB_PASSWORD'),
                    allow_temp_tables=temp_tables)

def get_ms_dbc_instance(section_prefix=None, temp_tables=True):
        """
        Gets a new MS SQL Server DbConnect, reading parameters from config
        """
        config = ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + "\\db_config.cfg")
        sec_str = 'SQL_DB'
        if section_prefix is not None:
            sec_str = f'{section_prefix}_{sec_str}'
        return psdb3.DbConnect(type='MS',
                    server=config.get(sec_str, 'SERVER'),
                    database=config.get(sec_str, 'DB_NAME'),
                    user=config.get(sec_str, 'DB_USER'),
                    password=config.get(sec_str, 'DB_PASSWORD'),
                    allow_temp_tables=temp_tables)

def drop_all_tables_ms(ms, schema='dbo'):
    """
    Drops all tables in an MSSQL database in the given schema.
    Source: mssqltips.com/sqlservertip/6798/drop-all-tables-sql-server
    """
    query = f"""USE [{schema}.{ms.dbname}]
    GO;
    SELECT 'ALTER TABLE'
        + OBJECT_SCHEMA_NAME(parent_object_id)
        + '.'
        + QUOTENAME(OBJECT_NAME(parent_object_id))
        + ' '
        + 'DROP CONSTRAINT'
        + QUOTENAME(name)
    FROM sys.foreign_keys
    ORDER BY OBJECT_SCHEMA_NAME(parent_object_id), OBJECT_NAME(parent_object_id);
    GO;
    """
    ms.query(query)

def drop_all_tables_pg(pg, schema='working'):
    """
    Drops all tables in a postgresql database
    Source: http://stackoverflow.com/questions/3327312/ddg#13823560
    """
    query = f""" DROP SCHEMA {schema} CASCADE;
    CREATE SCHEMA {schema};
    GRANT ALL ON SCHEMA {schema} TO postgres;
    GRANT ALL ON SCHEMA {schema} TO {schema};
    """
    pg.query(query)