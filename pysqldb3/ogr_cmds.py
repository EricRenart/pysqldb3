from osgeo import ogr, gdal
from typing import List, Optional
import os
from . import Config
from . import util
import subprocess
import logging

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
    gdal_data = Config.get_gdal_data_path()
    
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
    db_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    dbhost = db_config.get('SERVER')
    dbport = db_config.get('PORT')
    dbname = db_config.get('DB_NAME')
    dbuser = db_config.get('DB_USER')
    dbpass = db_config.get('DB_PASSWORD')
    
    # Construct neccessary command
    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -nlt PROMOTE_TO_MULTI -overwrite
        -a_srs 'EPSG:{srid}' -progress -f PostgreSQL 'PG:"host={dbhost} port={dbport} dbname={dbname} user={dbuser} 
        password={dbpass}"' {shp_path} -nln {schema}.{tbl_name}"""

    # Execute command
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)

    query_result = subprocess.check_output(ogr_command)
    if capture_output:
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
    gdal_data = Config.get_gdal_data_path()

    # Connect to db
    db_config = Config.read_config('tests\\db_config.cfg').get('MS_DB')
    dbhost = db_config.get('SERVER')
    dbname = db_config.get('DB_NAME')
    dbuser = db_config.get('DB_USER')
    dbpass = db_config.get('DB_PASSWORD')

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
    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -nlt PROMOTE_TO_MULTI
        -overwrite -a_srs "EPSG:{srid}" -progress -f MSSQLSpatial
        'MSSQL:"server={dbhost}; database={dbname}; UID={dbuser}; PWD={dbpass}"' {shp_path} -nln {schema}.{tbl_name}"""
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)


    # execute query
    query_result = subprocess.check_output(ogr_command)
    if capture_output:
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
    gdal_data = Config.get_gdal_data_path()
    
    # Get db login credentials
    db_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    dbhost = db_config.get('SERVER')
    dbport = db_config.get('PORT')
    dbname = db_config.get('DB_NAME')
    dbuser = db_config.get('DB_USER')
    dbpass = db_config.get('DB_PASSWORD')

    # Construct neccesary command
    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -overwrite -f 'ESRI Shapefile'
        {export_path}\{shp_name} -a_srs "EPSG:{srid}" 'PG:"host={dbhost} port={dbport} dbname={dbname} user={dbuser}
        password={dbpass}"' -sql {tbl_name}"""
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)

    # execute query
    query_result = subprocess.check_output(ogr_command)
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
    gdal_data = Config.get_gdal_data_path()

    # Get db login credentials
    db_config = Config.read_config('tests\\db_config.cfg').get('MS_DB')
    dbhost = db_config.get('SERVER')
    dbname = db_config.get('DB_NAME')
    dbuser = db_config.get('DB_USER')
    dbpass = db_config.get('DB_PASSWORD')

    # Construct neccessary command
    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -overwrite -f 'ESRI Shapefile'
        {export_path}\{shp_name} -a_srs "EPSG:{srid}" 'MSSQL:"server={dbhost}; database={dbname}; UID={dbuser}; 
        PWD={dbpass}"' -sql {tbl_name}"""
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)

    # execute query
    query_result = subprocess.check_output(ogr_command)
    if capture_output:
        return query_result

"""
Feature Class OGR Commands
"""

def read_feature_class_pg(fc_name=None, geodatabase=None, tbl_name=None, schema='working', srid=2263, capture_output=False):
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
    db_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    dbhost = db_config.get('SERVER')
    dbport = db_config.get('PORT')
    dbname = db_config.get('DB_NAME')
    dbuser = db_config.get('DB_USER')
    dbpass = db_config.get('DB_PASSWORD')

    # construct neccessary command
    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -nlt PROMOTE_TO_MULTI -overwrite
    -progress -f "ESRI Shapefile" PostgreSQL 'PG:"host={dbhost} port={dbport} dbname={dbname} user={dbuser} password={dbpass}"'
    {geodatabase} {fc_name} -nln {schema}.{tbl_name}"""
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)

    # execute query
    query_result = subprocess.check_output(ogr_command)
    if capture_output:
        return query_result

    

def read_feature_class_ms(fc_name=None, geodatabase=None, tbl_name=None, schema='dbo', srid=2263, capture_output=False):
    # type: (str, str, str, str, int, bool) -> Optional(str)
    """
    Read in a Feature Class to the MSSQL database.
    :param fc_name: Name of the feature class to read in
    :param geodatabase: The geodatabase path to read in the feature class from
    :param tbl_name: The name of the table to store feature class data in.
    :param schema: The db schema to use. Default 'public'
    :param srid: Spatial reference identifier for coordinate system to use (default 2263 NAD83/NYLI-ft)
    :param capture_output: Whether to return the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()

    # Get db login credentials
    db_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    dbhost = db_config.get('SERVER')
    dbname = db_config.get('DB_NAME')
    dbuser = db_config.get('DB_USER')
    dbpass = db_config.get('DB_PASSWORD')

    ogr_command = f"""ogr2ogr --config GDAL_DATA {Config.get_gdal_data_path} -overwrite -progress -f "ESRI Shapefile"
    MSSQLSpatial 'MSSQL:"server={dbhost}; database={dbname}; UID={dbuser}; PWD={dbpass}"' {geodatabase} {fc_name}
    -nln {schema}.{tbl_name}"""
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)

    # execute command
    query_result = subprocess.check_output(ogr_command)
    if capture_output:
        return query_result

"""
DB-DB IO Commands
"""
def pgsql_to_mssql(pg_table=None, ms_table=None, pg_schema='working', ms_schema='dbo', use_ldap=False, spatial=False, srid=2263, capture_output=False):
    # type: (str, str, str, str, bool, bool, int, bool) -> Optional(str)
    """
    Export a table from a PostgreSQL database to a MSSQL Server database.
    :param source_table: The name of the source PostgreSQL table to convert to MSSQL.
    :param dest_table: The name of the destination MSSQL table to be created.
    :param pg_schema: Database schema to use for source PostgreSQL database (default 'public')
    :param ms_schema: Database schema to use for destination MSSQL database (default 'public')
    :param use_ldap: Whether to use Lightweight Directory Access Protocol (LDAP) for db connection. (default False)
    :param spatial: Flag for spatial table (defaults to True)
    :param srid: The SRID number for the CRS to use, default 2263 (NAD83-NYLI-ft)
    :param capture_output: Whether to return the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get login credentials for databases
    pg_db_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    ms_db_config = Config.read_config('tests\\db_config.cfg').get('MS_DB')

    ms_dbhost = ms_db_config.get('SERVER')
    ms_dbname = ms_db_config.get('DB_NAME')
    ms_dbuser = ms_db_config.get('DB_USER')
    ms_dbpass = ms_db_config.get('DB_PASSWORD')

    pg_dbhost = pg_db_config.get('SERVER')
    pg_dbport = pg_db_config.get('PORT')
    pg_dbname = pg_db_config.get('DB_NAME')
    pg_dbuser = pg_db_config.get('DB_USER')
    pg_dbpass = pg_db_config.get('DB_PASSWORD')

    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -overwrite -progress -f 
    MSSQLSpatial 'MSSQL:"server={ms_dbhost}; database={ms_dbname}; UID={ms_dbuser}; PWD={ms_dbpass}"' 
    'PG:"host={pg_dbhost} port={pg_dbport} dbname={pg_dbname} user={pg_dbuser} password={pg_dbpass}"'
    {pg_schema}.{pg_table} -lco OVERWRITE=yes -nln {ms_schema}.{ms_table} """

    if spatial:
        ogr_command += f"-a_srs 'EPSG:{srid}' "
    else:
        ogr_command += "-nlt NONE "
    ogr_command += "-progress --config MSSQLSPATIAL_USE_GEOM_COLUMNS NO"
    logging.info('Executing the following OGR command:')
    logging.info(str(ogr_command))
    # excecute query
    query_result = subprocess.check_output(ogr_command)
    if capture_output:
        return query_result
    

def mssql_to_pgsql(ms_table=None, pg_table=None, ms_schema='dbo', pg_schema='working', use_ldap=False, spatial=False, as_query=True, srid=2263, capture_output=False):
    # type: (str, str, str, str, bool, bool, bool, int, bool) -> Optional(str)
    """
    Export a table from a MS SQL Server database to a PostgreSQL database.
    :param source_table: The name of the source MSSQL table to convert to PostgreSQL.
    :param dest_table: The name of the destination PostgreSQL table to be created.
    :param pg_schema: Database schema to use for destination PostgreSQL database (default 'public')
    :param ms_schema: Database schema to use for source MSSQL database (default 'public')
    :param use_ldap: Whether to use Lightweight Directory Access Protocol (LDAP) for db connection. (default False)
    :param as_query: Whether to run this command as an SQL Query (default False)
    :param srid: The SRID number for the CRS to use, default 2263 (NAD83-NYLI-ft)
    :param capture_output: Whether to return the results of the SQL query (default False)
    """
# Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get login credentials for databases
    pg_db_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    ms_db_config = Config.read_config('tests\\db_config.cfg').get('MS_DB')

    ms_dbhost = ms_db_config.get('SERVER')
    ms_dbname = ms_db_config.get('DB_NAME')
    ms_dbuser = ms_db_config.get('DB_USER')
    ms_dbpass = ms_db_config.get('DB_PASSWORD')

    pg_dbhost = pg_db_config.get('SERVER')
    pg_dbport = pg_db_config.get('PORT')
    pg_dbname = pg_db_config.get('DB_NAME')
    pg_dbuser = pg_db_config.get('DB_USER')
    pg_dbpass = pg_db_config.get('DB_PASSWORD')

    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -overwrite -progress -f
    'PG:"host={pg_dbhost} port={pg_dbport} dbname={pg_dbname} user={pg_dbuser} password={pg_dbpass}"'
    MSSQLSpatial 'MSSQL:"server={ms_dbhost}; database={ms_dbname}; UID={ms_dbuser}; PWD={ms_dbpass}"' 
    {ms_schema}.{ms_table} -lco OVERWRITE=yes -nln {pg_schema}.{pg_table} """

    if spatial:
        ogr_command += f"-a_srs 'EPSG:{srid}' "
    else:
        ogr_command += "-nlt NONE "
    ogr_command += "--config MSSQLSPATIAL_USE_GEOM_COLUMNS NO"
    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)
    # excecute query
    query_result = subprocess.check_output(ogr_command)
    if capture_output is not None:
        return query_result


def pgsql_to_pgsql(source_table=None, dest_table=None, source_schema='public', dest_schema='public', sql_query=None, spatial=True, srid=2263, capture_output=False):
    # type: (str, str, str, str, bool, bool, int, bool) -> Optional(str)
    """
    Export a table from a PostgreSQL database to another PostgreSQL database.
    :param source_table: The name of the source PostgreSQL table to export.
    :param dest_table: Name of the table to be created in the destination PostgreSQL database.
    :param source_schema: Schema of the source table (default 'public')
    :param dest_schema: Schema of the destination table (default 'public')
    :param sql_query: SQL Query to run on source db
    :param use_ldap: Whether to use Lightweight Directory Access Protocol (LDAP) for db connection. (default False)
    :param spatial: Flag for spatial table (defaults to True)
    :param srid: The SRID number for the CRS to use, default 2263 (NAD83-NYLI-ft)
    :param capture_output: Whether to return the results of the SQL query (default False)
    """
    # Make gdal throw exceptions
    gdal.UseExceptions()
    gdal_data = Config.get_gdal_data_path()

    # Get login credentials for db
    db1_config = Config.read_config('tests\\db_config.cfg').get('PG_DB')
    db1_host = db1_config.get('SERVER')
    db1_port = db1_config.get('PORT')
    db1_name = db1_config.get('DB_NAME')
    db1_user = db1_config.get('DB_USER')
    db1_pass = db1_config.get('DB_PASSWORD')

    # destination db
    db2_config = Config.read_config('tests\\db_config.cfg').get('SECOND_PG_DB')
    db2_host = db2_config.get('SERVER')
    db2_port = db2_config.get('PORT')
    db2_name = db2_config.get('DB_NAME')
    db2_user = db2_config.get('DB_USER')
    db2_pass = db2_config.get('DB_PASSWORD')

    ogr_command = f"""ogr2ogr --config GDAL_DATA {gdal_data} -overwrite -progress -f "PostgreSQL"
    'PG:"host={db1_host} port={db1_port} dbname={db1_name} user={db1_user} password={db1_pass}"'
    'PG:"host={db2_host} port={db2_port} dbname={db2_name} user={db2_user} password={db2_pass}"'
    -lco OVERWRITE=yes -nln {dest_schema}.{dest_table} """
    if sql_query is not None:
        ogr_command += f"-sql {sql_query} "
    if spatial:
        ogr_command += f"-a_srs 'EPSG:{srid}'"

    logging.info('Executing the following OGR command:')
    logging.info(ogr_command)

    # execute command
    result = subprocess.check_output(ogr_command)
    if result is not None:
        return result

"""
Bulk File Commands
"""
def pg_bulk_file_to_table(paths, dest_table, schema='public', capture_output=False):
    # type: (List(str), str, str, bool) -> Optional(str)
    """
    Imports bulk data to a PostgreSQL database table.
    :param paths: List of filepaths to import into table
    :param dest_table: Name of table to be created in destination database
    :param schema: Database schema to use for import, default 'public'
    :param capture_output: Whether to return the results of the SQL query (default False)
    """
    pass

def ms_bulk_file_to_table(paths, dest_table, schema='public', capture_output=False):
    # type: (List(str), str, str, bool) -> Optional(str)
    """
    Imports bulk data to an MS SQL Server database table.
    :param paths: List of filepaths to import into table
    :param dest_table: Name of table to be created in destination database
    :param schema: Database schema to use for import, default 'public'
    :param capture_output: Whether to return the results of the SQL query (default False)
    """
    pass