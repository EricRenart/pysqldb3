from osgeo import ogr, gdal
from typing import List, Optional
import os
import Config
import subprocess
import util

"""
ogr_cmds.py
This file contains functions for performing queries with GDAL and OGR.
"""

def _get_geom_name_from_ogr_type(ogr_type):
    """
    Converts OGR geometry types to geometry type names.
    """
    name_type_dict = {ogr.wkbUnknown: "UNKNOWN",
    ogr.wkbLineString: "POINT",
    ogr.wkbPolygon: "LINESTRING",
    ogr.wkbMultiPoint: "MULTIPOINT",
    ogr.wkbMultiLineString: "MULTILINESTRING",
    ogr.wkbMultiPolygon: "MULTIPOLYGON",
    ogr.wkbGeometryCollection: "GEOMETRYCOLLECTION",
    ogr.wkbNone: "NONE",
    ogr.wkbLinearRing: "LINEARRING"}
    return name_type_dict.get(ogr_type)


"""
Shapefile OGR Commands
"""
def read_shapefile_pg(shp_path=None, tbl_name=None, schema='public', srid=2263, capture_output=False):
    # type: (str, str, str, int, bool) -> Optional(str)
    """
    Read in an ESRI shapefile and store its data in the PostgreSQL database.
    :param shp_path: Path to the shapefile to be read
    :param tbl_name: Name of table in database to store shapefile data in
    :param schema: Database schema to use, default 'public'
    :param srid: Spatial reference identifier for coordinate system to use (default 2263)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    
    # Check for errors
    if not os.path.isfile(shp_path):
        raise FileNotFoundError('read_shapefile_pg(): file not found')
    if not shp_path.endswith('.shp'):
        raise TypeError('read_shapefile_pg(): provided path is not a Shapefile')

    # Open the shapefile
    shapefile_ds = ogr.GetDriverByName('ESRI Shapefile').Open(shp_path)
    layer = shapefile_ds.GetLayer(0)
    geo_type = layer.GetLayerDefn().GetGeomType()
    geo_name = _get_geom_name_from_ogr_type(geo_type)

    # Connect to db
    db_config = Config.read_config('tests/db_config.cfg').get('PG_DB')
    dbhost = db_config.get('host')
    dbport = db_config.get('port')
    dbname = db_config.get('dbname')
    dbuser = db_config.get('user')
    dbpass = db_config.get('password')
    
    # Construct neccessary command
    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', Config.get_gdal_data_path(),
    '-nlt', 'PROMOTE_TO_MULTI', '-overwrite', '-a_srs', f"EPSG:{srid}", '-progress',
    '-f', 'PostgreSQL', f'PG:"host={dbhost} port={dbport} dbname={dbname} user={dbuser} password={dbpass}"',
    {shp_path}, '-nln', f'{schema}.{tbl_name}']

    # Execute command
    query_result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result


def read_shapefile_ms(shp_path=None, tbl_name=None, schema='public', srid=2263, capture_output=False):
    # type: (str, str, str, int, bool) -> Optional(str)
    """
    Read in an ESRI shapefile and store its data in the MSSQL database.
    :param shp_path: Path to the shapefile to be read
    :param tbl_name: Name of table in database to store shapefile data in
    :param schema: Database schema to use, default 'public'
    :param srid: Spatial reference identifier for coordinate system to use (default 2263)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()

    # Connect to db
    db_config = Config.read_config('tests/db_config.cfg').get('MS_DB')
    dbhost = db_config.get('host')
    dbname = db_config.get('dbname')
    dbuser = db_config.get('user')
    dbpass = db_config.get('password')

    # Check for errors
    if not os.path.isfile(shp_path):
        raise FileNotFoundError('read_shapefile_pg(): file not found')
    if not shp_path.endswith('.shp'):
        raise TypeError('read_shapefile_pg(): provided path is not a Shapefile')

    # Open the shapefile
    shapefile_ds = ogr.GetDriverByName('ESRI Shapefile')
    layer = shapefile_ds.GetLayer(0)
    geo_type = layer.GetLayerDefn().GetGeomType()
    geo_name = _get_geom_name_from_ogr_type(geo_type)

    # Construct neccessary command
    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', Config.get_gdal_data_path(),
    '-nlt','PROMOTE_TO_MULTI','-overwrite','-a_srs', f'EPSG:{srid}', 
    '-progress', '-f', 'MSSQLSpatial', f"MSSQL:server={dbhost}; port={dbport}; database={dbname}; \
     UID={dbuser}; PWD={dbpass}", {shp_path}, '-nln', f'{schema}.{tbl_name}']

    # execute query
    query_result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result
    

def write_shapefile_pg(shp_name=None, tbl_name=None, export_path=None, srid=2263, capture_output=False):
    # type: (str, str, str, int, bool) -> Optional(str)
    """
    Write out an ESRI Shapefile using data from the PostgreSQL database.
    :param shp_name: Filename of the shapefile to be created.
    :param tbl_name: Name of the table in origin PostgreSQL db to write a shapefile from.
    :param export_path: Folder path to write out the shapefile to.
    :param srid: Spatial reference identifier for coordinate system to use (default 2263 NAD83/NYLI-ft)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    
    # Get db login credentials
    db_config = Config.read_config('tests/db_config.cfg').get('PG_DB')
    dbhost = db_config.get('host')
    dbport = db_config.get('port')
    dbname = db_config.get('dbname')
    dbuser = db_config.get('user')
    dbpass = db_config.get('password')

    # Construct neccesary command
    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', Config.get_gdal_data_path(),
    '-overwrite', '-f', 'ESRI Shapefile', f'{export_path}\{shp_name}', '-a_srs',
    f'EPSG:{srid}', f'PG:"host={dbhost} port={dbport} dbname={dbname} user={dbuser} password={dbpass}"',
    '-sql', f'{tbl_name}']

    # execute query
    query_result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result



def write_shapefile_ms(shp_name=None, tbl_name=None, export_path=None, srid=2263, capture_output=False):
    # type: (str, str, str, int, bool) -> Optional(str)
    """
    Write out an ESRI Shapefile using data from the MSSQL database.
    :param shp_name: Filename of the shapefile to be created.
    :param tbl_name: Name of the table in origin MS SQL Server db to write a shapefile from.
    :param export_path: Folder path to write out the shapefile to.
    :param srid: Spatial reference identifier for coordinate system to use (default 2263 NAD83/NYLI-ft)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    :return: Path to shapefile on disk
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()

    # Get db login credentials
    db_config = Config.read_config('tests/db_config.cfg').get('MS_DB')
    dbhost = db_config.get('host')
    dbname = db_config.get('dbname')
    dbuser = db_config.get('user')
    dbpass = db_config.get('password')

    # Construct neccessary command
    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', Config.get_gdal_data_path(),
    '-overwrite', '-f', 'ESRI Shapefile', f'{export_path}\{shp_name}', '-a_srs',
    f'EPSG:{srid}', f"MSSQL:server={dbhost}; database={dbname}; UID={dbuser}; PWD={dbpass}",
    '-sql', f'{tbl_name}']

    # execute query
    query_result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result

"""
Feature Class OGR Commands
"""

def read_feature_class_pg(fc_name=None, geodatabase=None, tbl_name=None, schema='public', srid=2263, capture_output=False):
    # type: (str, str, str, str, int, bool) -> Optional(str)
    """
    Read in a Feature Class to the Postgre database.
    :param fc_name: Name of the feature class to read in
    :param geodatabase: The geodatabase path to read in the feature class from
    :param tbl_name: The name of the table to store feature class data in.
    :param schema: The db schema to use. Default 'public'
    :param srid: Spatial reference identifier for coordinate system to use (default 2263 NAD83/NYLI-ft)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """

    # Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get db login credentials
    db_config = Config.read_config('tests/db_config.cfg').get('PG_DB')
    dbhost = db_config.get('host')
    dbport = db_config.get('port')
    dbname = db_config.get('dbname')
    dbuser = db_config.get('user')
    dbpass = db_config.get('password')

    # construct neccessary command
    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', Config.get_gdal_data_path(),
    '-nlt','PROMOTE_TO_MULTI', '-overwrite', '-f', 'ESRI Shapefile', 
    f'PostgreSQL', f'PG:"host={dbhost} port={dbport} dbname={dbname} user={dbuser} password={dbpass}"',
    {geodatabase}, {fc_name}, '-nln', f'{schema}.{tbl_name}', '-progress']

    # execute query
    query_result = subprocess.call(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result

    

def read_feature_class_ms(fc_name=None, geodatabase=None, tbl_name=None, schema='public', srid=2263, capture_output=False):
    # type: (str, str, str, str, int, bool) -> Optional(str)
    """
    Read in a Feature Class to the MSSQL database.
    :param fc_name: Name of the feature class to read in
    :param geodatabase: The geodatabase path to read in the feature class from
    :param tbl_name: The name of the table to store feature class data in.
    :param schema: The db schema to use. Default 'public'
    :param srid: Spatial reference identifier for coordinate system to use (default 2263 NAD83/NYLI-ft)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()

    # Get db login credentials
    db_config = Config.read_config('tests/db_config.cfg').get('PG_DB')
    dbhost = db_config.get('host')
    dbport = db_config.get('port')
    dbname = db_config.get('dbname')
    dbuser = db_config.get('user')
    dbpass = db_config.get('password')

    # construct neccessary command
    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', Config.get_gdal_data_path(),
    '-overwrite', '-f', 'ESRI Shapefile', f'MSSQLSpatial', 
    f'"MSSQL:server={dbhost}; port={dbport}; database={dbname}; UID={dbuser}; PWD={dbpass}"',
    {geodatabase}, {fc_name}, '-nln', f'{schema}.{tbl_name}', '-progress']

    # execute query
    query_result = subprocess.call(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result



"""
DB-DB IO Commands
"""
def pgsql_to_mssql(pg_table=None, ms_table=None, pg_schema='public', ms_schema='public', use_ldap=False, spatial=False, capture_output=False):
    # type: (str, str, str, str, bool, bool, bool) -> Optional(str)
    """
    Export a table from a PostgreSQL database to a MSSQL Server database.
    :param source_table: The name of the source PostgreSQL table to convert to MSSQL.
    :param dest_table: The name of the destination MSSQL table to be created.
    :param pg_schema: Database schema to use for source PostgreSQL database (default 'public')
    :param ms_schema: Database schema to use for destination MSSQL database (default 'public')
    :param use_ldap: Whether to use Lightweight Directory Access Protocol (LDAP) for db connection. (default False)
    :param spatial: Flag for spatial table (defaults to True)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get login credentials for databases
    pg_db_config = Config.read_config('tests/db_config.cfg').get('PG_DB')
    ms_db_config = Config.read_config('tests/db_config.cfg').get('MS_DB')

    ms_dbhost = ms_db_config.get('SERVER')
    ms_dbname = ms_db_config.get('DB_NAME')
    ms_dbuser = ms_db_config.get('DB_USER')
    ms_dbpass = ms_db_config.get('DB_PASSWORD')

    pg_dbhost = pg_db_config.get('SERVER')
    pg_dbport = pg_db_config.get('PORT')
    pg_dbname = pg_db_config.get('DB_NAME')
    pg_dbuser = pg_db_config.get('DB_USER')
    pg_dbpass = pg_db_config.get('DB_PASSWORD')

    ogr_command = ['ogr2ogr','--config','GDAL_DATA',f'"{gdal_data}"','-overwrite',
    '-f','MSSQLSpatial',f'"MSSQL:server={ms_dbhost}; database={ms_dbname}; UID={ms_dbuser}; PWD={ms_dbpass}"',
    f'PG:"host={pg_dbhost} port={pg_dbport} dbname={pg_dbname} user={pg_dbuser} pass={pg_dbpass}"',
    f"{pg_schema}.{pg_table}", '-lco', 'OVERWRITE=yes', '-nln', f'{ms_schema}.{ms_table}']

    if spatial:
        ogr_command.append(['-a_srs','EPSG:2263'])
    else:
        ogr_command.append([' ','-nlt','NONE'])

    ogr_command.append(['-progress', '--config', 'MSSQLSPATIAL_USE_GEOMETRY_COLUMNS', 'NO'])

    # excecute query
    query_result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result
    

def mssql_to_pgsql(ms_table=None, pg_table=None, ms_schema='public', pg_schema='public', use_ldap=False, spatial=False, as_query=True, capture_output=False):
    # type: (str, str, str, str, bool, bool, bool, bool) -> Optional(str)
    """
    Export a table from a MS SQL Server database to a PostgreSQL database.
    :param source_table: The name of the source MSSQL table to convert to PostgreSQL.
    :param dest_table: The name of the destination PostgreSQL table to be created.
    :param pg_schema: Database schema to use for destination PostgreSQL database (default 'public')
    :param ms_schema: Database schema to use for source MSSQL database (default 'public')
    :param use_ldap: Whether to use Lightweight Directory Access Protocol (LDAP) for db connection. (default False)
    :param as_query: Whether to run this command as an SQL Query (default False)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get login credentials for databases
    pg_db_config = Config.read_config('tests/db_config.cfg').get('PG_DB')
    ms_db_config = Config.read_config('tests/db_config.cfg').get('MS_DB')

    ms_dbhost = ms_db_config.get('SERVER')
    ms_dbname = ms_db_config.get('DB_NAME')
    ms_dbuser = ms_db_config.get('DB_USER')
    ms_dbpass = ms_db_config.get('DB_PASSWORD')

    pg_dbhost = pg_db_config.get('SERVER')
    pg_dbport = pg_db_config.get('PORT')
    pg_dbname = pg_db_config.get('DB_NAME')
    pg_dbuser = pg_db_config.get('DB_USER')
    pg_dbpass = pg_db_config.get('DB_PASSWORD')

    ogr_command = ['ogr2ogr','--config','GDAL_DATA',f'"{gdal_data}"','-overwrite',
    '-f','PostgreSQL',f'PG:"host={pg_dbhost} port={pg_dbport} dbname={pg_dbname} user={pg_dbuser} password={pg_dbpass}',
    '-f', 'MSSQLSpatial',f'"MSSQL:server={ms_dbhost}; database={ms_dbname}; UID={ms_dbuser}; PWD={ms_dbpass}"',
    f'{ms_schema}.{ms_table}', '-lco', 'OVERWRITE=yes', '-nln', f'{pg_schema}.{pg_table}']
    if spatial:
        ogr_command.append(['EPSG:2263'])
    ogr_command.append(['-progress'])

    # excecute query
    query_result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if query_result is not None:
        return query_result


def pgsql_to_pgsql(source_table=None, dest_table=None, source_schema='public', dest_schema='public', sql_query=None, spatial=True, capture_output=False):
    # type: (str, str, str, str, bool, bool, bool) -> Optional(str)
    """
    Export a table from a PostgreSQL database to another PostgreSQL database.
    :param source_table: The name of the source PostgreSQL table to export.
    :param dest_table: Name of the table to be created in the destination PostgreSQL database.
    :param source_schema: Schema of the source table (default 'public')
    :param dest_schema: Schema of the destination table (default 'public')
    :param sql_query: SQL Query to run on source db
    :param use_ldap: Whether to use Lightweight Directory Access Protocol (LDAP) for db connection. (default False)
    :param spatial: Flag for spatial table (defaults to True)
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get login credentials for db
    db1_config = Config.read_config('/tests/db_config.cfg').get('PG_DB')
    db1_host = db1_config.get('SERVER')
    db1_port = db1_config.get('PORT')
    db1_name = db1_config.get('DB_NAME')
    db1_user = db1_config.get('DB_USER')
    db1_pass = db1_config.get('DB_PASSWORD')

    # destination db
    db2_config = Config.read_config('/tests/db_config.cfg').get('SECOND_PG_DB')
    db2_host = db2_config.get('SERVER')
    db2_port = db2_config.get('PORT')
    db2_name = db2_config.get('DB_NAME')
    db2_user = db2_config.get('DB_USER')
    db2_pass = db2_config.get('DB_PASSWORD')

    ogr_command = ['ogr2ogr', '--config', 'GDAL_DATA', {gdal_data}, '-overwrite', '-f',
    '"PostgreSQL"', f'PG:"host={db2_host} port={db2_port} dbname={db2_name} user={db2_user} password={db2_pass}"',
    f'PG:"host={db1_host} port={db1_port} dbname={db1_name} user={db1_user} password={db1_pass}"', f'{source_schema}.{source_table}',
    '-lco', 'OVERWRITE=yes', '-nln', f'{dest_schema}.{dest_table}']

    if sql_query is not None:
        ogr_command.append(['-sql', sql_query])

    if spatial:
        ogr_command.append(['EPSG:2263'])
    
    ogr_command.append(['-progress'])

    # execute command
    result = subprocess.check_output(ogr_command, capture_output=capture_output)
    if result is not None:
        return result

"""
Bulk File Commands
"""
def pg_bulk_file_to_table(paths, dest_table, schema='public', capture_output=False):
    # type: (List(str), str, str, bool) -> Optional(str)
    """
    Imports bulk data to a PostgreSQL database table.
    :param paths: List of filepaths to import into table (corresponds to )
    :param dest_table: Name of table to be created in destination database
    :param schema: Database schema to use for import, default 'public'
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    pass

def ms_bulk_file_to_table(paths, dest_table, schema='public', capture_output=False):
    # type: (List(str), str, str, bool) -> Optional(str)
    """
    Imports bulk data to an MS SQL Server database table.
    :param paths: List of filepaths to import into table (corresponds to )
    :param dest_table: Name of table to be created in destination database
    :param schema: Database schema to use for import, default 'public'
    :param capture_output: Whether to print out the results of the SQL query (default False)
    """
    pass