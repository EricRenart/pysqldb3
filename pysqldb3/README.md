## RIS Library Components 

## 1. Pysqldb3 (DbConnect) - pysqldb3.py
Pysqldb3 contains `DbConnect`, a class built off of `pydodbc/psycopg2` that makes it easy to connect to Postgres/Sql Server databases in Python. 
### 1.1 Simple Example/Setup  
To create a `DbConnect` object:
1. `import pysqldb3`
2. `db = pysqldb.DbConnect(type='PG', server='server_name', database='db_name')` 
    + Replace `server_name` and `db_name` with the actual values. 
    + You must specify the type, either `PG` (Postgres) or `MS` (SQL Server). 
    + You can also add your username using `user='my_username'` 
    + You can add your password similarly using `password='my_password'`
    + Other inputs include LDAP and ports. If you're unsure about these, feel free to ask around. 
3. Now, you can query on your database by using `db.query('select * from my_schema.my_table')`

### 1.2 Functions 
In Jupyter or Python shell, use `help(pysqldb3)` to show all public functions and their inputs. <br>
#### pysqldb public functions:

1. [`connect`](#connect): Connects to database
1. [`disconnect`](#disconnect): Disconnects from database.  
1. [`check_conn`](#check_conn): Checks and reconnects to connection if not currently connected.
1. [`log_temp_table`](#log_temp_table-table-owner-servernone-databasenone-expirationdatetimedatetimenow--datetimetimedeltadays7): Writes tables to temp log to be deleted after expiration date.
1. [`check_logs`](#check_logs): Queries the temp log associated with the user's login and returns a pandas `DataFrame` of results. 
1. [`clean_up_new_tables`](#clean_up_new_tables): Drops all newly created tables from this `DbConnect` instance (current session).
1. [`blocking_me`](#blocking_me): Queries database to check for queries or users currently blocking the user (defined in the connection). *Postgres Only.*
1. [`kill_blocks`](#kill_blocks): Will kill any queries that are blocking, that the user (defined in the connection) owns. *Postgres Only*.
1. [`my_tables`](#my_tables): Get a list of tables for which user (defined in the connection) is the owner *Postgres Only*.
1. [`table_exists`](#table_exists): Checks if table exists in the database. 
1. [`get_schemas`](#get_schemas): Gets a list of schemas available in the database.
1. [`get_table_columns`](#get_table_columns): Gets a list of columns and their datatypes for a specified table.
1. [`query`](#query): Runs query from input SQL string, calls `Query` object. 
1. [`drop_table`](#drop_table):  Drops table from database and removes from the temp log table
1. [`rename_column`](#rename_column): Renames a column to the new column name on the specified table.
1. [`dfquery`](#dfquery): Runs from input SQL string, calls `Query` object with `return_df=True`; returns Pandas `DataFrame`
1. [`print_last_query`](#print_last_query): Prints latst query run with basic formatting
1. [`dataframe_to_table_schema`](#dataframe_to_table_schema): Translates Pandas `DataFrame` into empty database table.
1. [`dataframe_to_table`](#dataframe_to_table): Adds data from Pandas `DataFrame` to existing table
1. [`csv_to_table`](#csv_to_table): Imports csv file to database. This uses pandas datatypes to generate the table schema.
1. [`xls_to_table`](#xls_to_table): Imports xls file to database. This uses pandas datatypes to generate the table schema.
1. [`query_to_csv`](#query_to_csv): Exports query results to a csv file.
1. [`query_to_map`](#query_to_map): Generates Plotly choropleth map using the query results.
1. [`query_to_shp`](#query_to_shp): Exports query results to an ESRI Shapefile file.
2. [`table_to_shp`](#table_to_shp): Exports database table to an ESRI Shapefile file.
1. [`table_to_csv`](#table_to_csv): Exports database table to an csv file.
1. [`shp_to_table`](#shp_to_table): Imports ESRI Shapefile to database, uses GDAL to generate the table.
1. [`feature_class_to_table`](#feature_class_to_table): Imports shape file feature class to database, uses GDAL to generate the table.

## Details 
### connect
**`DbConnect.connect(quiet=False)`**
Connects to database. This is automatically called when creating a database connection instance with `DbConnect`, 
it should not be needed to be manually called unless the database connection was closed. When called this will print 
database connection information. 
###### Parameters:
 - **`quiet`: bool, default False**: When `True`, does not print database connection information.
<!--  - **`user`: string, default None**: The username to use to connect to the database.
 - **`password`: string, default None**: The password to use to connect to the database.
 - **`ldap`: bool, default None**: Whether to use LDAP upon database connection.
 - **`type`: string, default None**: Type of database connection to use.
 - **`server`: string, default None**: The server hosting the database to connect to.
 - **`database`: string, default None**: The name of the database to connect to.
 - **`use_native_driver`: bool, default False**: Whether to use the native db driver when connecting.
 - **`port`: int, default 5432**: The port to use for the db connection.
 - **`default`: bool, default False** If true, automatically attempt to connect to the RIS database. -->
        
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.connect()

Database connection (PG) to ris on dotdevrhpgsql01 - user: shostetter 
Connection established 2021-08-04 10:28:34
- ris version 2.3.2 - 

>>> db.connect(quiet=False)

```
[Back to Table of Contents](#pysqldb-public-functions)


### disconnect
**`DbConnect.disconnect(quiet=False)`**
Disconnects from database. When called this will print database connection information and closed timestamp. 
###### Parameters:
 - **`quiet`: bool, default False**: When `True`, does not print database connection information. 

**Sample**
```
>>> import pysqldb3
>>> db = pysqldb.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.disconnect()

Database connection (PG) to ris on dotdevrhpgsql01 - user: shostetter 
Connection closed 2021-08-04 10:31:46

>>> db.disconnect(quiet=False)

```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### check_conn
**`DbConnect.check_conn()`**
Checks and reconnects to connection if not currently connected.

###### Parameters: 
- None

**Sample**
```
>>> import pysqldb3
>>> db = pysqldb.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.check_conn()

```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### log_temp_table
**`DbConnect.log_temp_table(schema, table, owner, server=None, database=None, expiration=datetime.datetime.now() + datetime.timedelta(days=7))`**
Writes tables to temp log to be deleted after expiration date. This method gets called automatically when a table is created by a `DbConnect` query. 
###### Parameters:
 - **`schema`: str**: Database schema name 
 - **`table`: str**: Table name to log
  - **`owner`: str**: userid of table owner
  - **`server`: str, default None**: Name of server, this is needed for queries that create tables on servers that are different from the `DbConnect` instance's server connection
  - **`database`: str, default None**: Name of database, this is needed for queries that create tables on servers that are different from the `DbConnect` instance's server connection
  - **`expiration`: datetime, default datetime.datetime.now() + datetime.timedelta(days=7)**: Date where table should be removed from the database. Defaults to seven days from current date.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

### check_logs
**`DbConnect.check_logs(schema=None)`**
Queries the temp log associated with the user's login and returns a pandas `DataFrame` of results.  Defaults to the `default_schema` database schema.
###### Parameters:
 - **`schema`: str, default None**: Database schema name. If none, use the default schema.

**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.check_logs(schema='working')

tbl_id table_owner table_schema             table_name          created_on     expires
3786  shostetter      working  seths_temp_test_table 2021-08-04 13:42:00  2021-08-11
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### clean_up_new_tables
**`DbConnect.clean_up_new_tables()`**
Drops all newly created tables from this `DbConnect` instance (current session).
###### Parameters:
 - None

**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.check_logs(schema='working')

Empty DataFrame
tbl_id table_owner table_schema             table_name          created_on     expires

>>> db.query("create table working.seths_temp_test_table as select 1 as dta")
- Query run 2021-08-04 13:42:25.171000
 Query time: Query run in 36000 microseconds
 * Returned 0 rows *
>>> db.check_logs(schema='working')

tbl_id table_owner table_schema             table_name          created_on     expires
3786  shostetter      working  seths_temp_test_table 2021-08-04 13:42:00  2021-08-11

>>> db.clean_up_new_tables()

Dropped 1 tables
>>> db.check_logs(schema='working')

Empty DataFrame
tbl_id table_owner table_schema             table_name          created_on     expires
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### blocking_me
**`DbConnect.blocking_me()`**
Queries database to check for queries or users currently blocking the user (defined in the connection). Postgres Only.
###### Parameters:
- None

**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.blocking_me()

Empty DataFrame
Columns: [blocked_pid, blocked_user, blocking_pid, blocking_user, blocked_statement, current_statement_in_blocking_process]
Index: []
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### kill_blocks
**`DbConnect.kill_blocks()`**
Will kill any queries that the user (defined in the connection) owns that are blocking. Postgres Only.
###### Parameters:
- None

**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.kill_blocks()

- Query run 2021-08-04 13:51:23.390000
 Query time: Query run in 7000 microseconds
 * Returned 0 rows *
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### my_tables
**`DbConnect.my_tables(schema='public')`**
Get a list of tables for which user (defined in the connection) is the owner Postgres Only.
###### Parameters:
 - **`schema`: str, default public**: Database schema name. Defaults to `public`.
 
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.my_tables(schema='working')

                        tablename  tableowner
0                      103_lights  shostetter
1               ___test___test___  shostetter
2                      sample_sig  shostetter
3   __temp_log_table_shostetter__  shostetter
4                   _tbl_updates_  shostetter
5                    bike_crashes  shostetter
6                        bike_inj  shostetter
7                   bike_vehicles  shostetter
8           corridor_retiming_oft  shostetter
9                 data_by_modzcta  shostetter
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### table_exists
**`DbConnect.table_exists(table, **kwargs)`**
Checks if table exists in the database
###### Parameters:
 - **`table`: str** Table name 
 - **`schema`: str, default None**: Database schema name. If `None`, defaults to the database's default schema.
 
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.table_exists('bike_inj', schema='working')

True
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### get_schemas
**`DbConnect.get_schemas()`**
Gets a list of schemas available in the database
###### Parameters:
 - None 
 
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.get_schemas()

['pg_catalog', 'information_schema', 'topology', 'working', 'staging', 'public', 'archive']
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### get_table_columns
**`DbConnect.get_table_columns()`**
Gets a list of columns and their data types in a specified table
##### Parameters:
 - **`table` str**: Name of table to be analyzed 
 - **`schema` str, default None**: If not provided, will assume database's default schema.
 - **`full` bool, default False**: If `True`, results will include all columns from `information_schema.columns` table, otherwise will be limited to name and data type.

 
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.get_table_columns('node')

[('ogc_fid', 'integer'),
 ('nodeid', 'numeric'),
 ('vintersect', 'character varying'),
 ('version', 'character varying'),
 ('created', 'timestamp with time zone'),
 ('masterid', 'integer'),
 ('is_int', 'boolean'),
 ('manual_fix', 'boolean'),
 ('is_cntrln_int', 'boolean'),
 ('geom', 'USER-DEFINED')]

```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### query
**`DbConnect.query(uery, strict=True, permission=True, temp=True, timeme=True, no_comment=False, comment='',
              lock_table=None, return_df=False, days=7)`**

Runs query from input SQL string, calls Query object.
###### Parameters:
 - **`query` str**: String sql query to be run
 - **`strict` bool, default True**: If `True` will run `sys.exit` on failed query attempts
 - **`permission` bool, default True**: If `False` it will override default will automatically grant select permissions on any tables created in the query
 - **`temp` bool, default True**: If `False` overrides default behavior where new tables will be logged for deletion at a future date
 - **`timeme` bool, default True**: If `False` overrides default behavior that automatically prints query duration time
 - **`no_comment` bool, default False**: If `True` overrides default behavior to automatically generate a comment on any tables created in query (Postgres only)
 - **`comment` str, default ''**: If provided, appends to automatic table generation comment
 - **`lock_table` str, default None**: ??? Table schema and name to be locked in format `'schema.table'`
 - **`return_df` bool, default False**: If `False` overrides default behavior where query results are stored and not returned, if True returns pandas DataFrame
 - **`days` int, default 7**: Defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted  
 
**Sample**

Create a table using query and verify that the table was recorded in the `tables_created` attribute
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("create table working.seths_temp_test_table as select 1 as dta, 2 as other_field")

- Query run 2021-08-04 16:09:25.171000
 Query time: Query run in 36000 microseconds
 * Returned 0 rows *
 
 >>> db.tables_created

['working.seths_temp_test_table']
```

Basic select query and verify that the results are stored in the `data` attribute
```
>>> db.query("select * from working.seths_temp_test_table")

- Query run 2021-08-04 16:10:56.926000
 Query time: Query run in 2000 microseconds
 * Returned 1 rows *
 
>>> db.data

[(1, 2)]
```

Multiple queries tied together 
```
>>> db.query("""
    drop table if exists working.seths_temp_test_table; 
    create table working.seths_temp_test_table as select 1 as dta, 2 as other_field;
    alter table working.seths_temp_test_table add column typ varchar;
    update working.seths_temp_test_table set typ = 'old';
    insert into working.seths_temp_test_table values (8, 9, 'new');
    select typ, count(*) as cnt from working.seths_temp_test_table   group by typ;
""")

- Query run 2021-08-04 16:46:18.539000
 Query time: Query run in 23000 microseconds
 * Returned 2 rows *

>>> db.data

[('old', 1L), ('new', 1L)]
```

Failed query in non-strict mode
```
>>> db.query("drop table working.seths_temp_test_table; select * from working.seths_temp_test_table", strict=False)

- Query failed: relation "working.seths_temp_test_table" does not exist
LINE 1: ...able working.seths_temp_test_table; select * from working.se...

- Query run 2021-08-04 16:19:45.485000
        drop table working.seths_temp_test_table; select * from working.seths_temp_test_table

```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### drop_table
**`DbConnect.drop_table(schema, table, cascade=False, strict=True, server=None, database=None)`**
Drops table if it exists from database and removes from the temp log table. If a table uses "" or [] because of case, spaces, or periods, they (""/[]) must be inputted explicitly.

###### Parameters:
 - **`schema`: str** Database schema name 
 - **`table`: str** Table name 
 - **`cascade`: bool, default False**: To drop a table that is referenced by a view or a foreign-key constraint of another table, `cascade=True` must be specified. Cascade will remove a dependent view entirely, but in the foreign-key case it will only remove the foreign-key constraint, not the other table entirely. (Postgres only)
 - **`strict` bool, default True**: May not be needed, but if set to `False` will prevent sys.exit on failed attempts
 - **`server`: str, default None**: Name of server, this is needed if tables to drop exist on servers that are different from the `DbConnect` instance's server connection
 - **`database`: str, default None**: Name of database, this is needed if tables to drop exist on servers that are different from the `DbConnect` instance's server connection

 
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("drop table if exists working.seths_temp_test_table;")

- Query run 2021-08-05 09:56:21.375000
 Query time: Query run in 4000 microseconds
 * Returned 0 rows *
 
>>> db.query("create table working.seths_temp_test_table as select 1 as dta, 2 as other_field;")

- Query run 2021-08-05 09:56:43.657000
 Query time: Query run in 71000 microseconds
 * Returned 0 rows *
 
 >>> db.table_exists('seths_temp_test_table', schema='working')
 
True
 
 >>> db.drop_table('working', 'seths_temp_test_table')
 
>>> db.table_exists('seths_temp_test_table', schema='working')
 
False
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>

### rename_column
**`DbConnect.rename_column(schema, table, old_column, new_column)`**
Renames a column to the new column name on the specified table.
###### Parameters:
 - **`schema`: str** Database schema name 
 - **`table`: str** Table name 
 - **`old_column`: str** Name of column to be renamed
 - **`new_column`: str** New column name
 
**Sample**
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("drop table if exists working.seths_temp_test_table;")

- Query run 2021-08-05 09:56:21.375000
 Query time: Query run in 4000 microseconds
 * Returned 0 rows *
 
>>> db.query("create table working.seths_temp_test_table as select 1 as dta, 2 as other_field;")

- Query run 2021-08-05 09:56:43.657000
 Query time: Query run in 71000 microseconds
 * Returned 0 rows *
 
 >>> db.rename_column('working', 'seths_temp_test_table', 'dta', 'new_column') 
 
 - Query run 2021-08-05 09:57:44.154000
 Query time: Query run in 35000 microseconds
 * Returned 0 rows *
 
 >>> db.dfquery("select * from working.seths_temp_test_table")
 
   new_column  other_field
0           1            2
```
[Back to Table of Contents](#pysqldb-public-functions)
<br>


### dfquery
**`DbConnect.dfquery(query, strict=True, permission=True, temp=True, timeme=True, no_comment=False, comment='',
              lock_table=None, return_df=False, days=7)`**

This is a wrapper for `Query`, to return a pandas `DataFrame`. This runs query from input SQL string, calls `Query` object with `return_df=True`. 
###### Parameters:
 - **`query` str**: String sql query to be run
 - **`strict` bool, defaut True**: If `True`, will run `sys.exit` on failed query attempts
 - **`permission` bool, default True**: If `False` it will override default will automatically grant select permissions on any tables created in the query
 - **`temp` bool, default True**: If `False` overrides default behavior where new tables will be logged for deletion at a future date
 - **`timeme` bool, default True**: If `False` overrides default behavior that automatically prints query durration time
 - **`no_comment` bool, default False**: If `True` overrides default behavior to automatically generate a comment on any tables created in query (Postgres only)
 - **`comment` str, default ''**: If provided, appends to automatic table generation comment
 - **`lock_table` str, default None**: ??? Table schema and name to be locked in format `'schema.table'` 
 - **`days` int, default 7**: Defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted  
 
**Sample**

Use query to set up sample table and dfquery to explore results in pandas.
```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("""
    drop table if exists working.seths_temp_test_table; 
    create table working.seths_temp_test_table as select 1 as dta, 2 as other_field;
    alter table working.seths_temp_test_table add column typ varchar;
    update working.seths_temp_test_table set typ = 'old';
    insert into working.seths_temp_test_table values (8, 9, 'new');
    select typ, count(*) as cnt from working.seths_temp_test_table   group by typ;
""")

- Query run 2021-08-05 10:39:00.759000
 Query time: Query run in 123000 microseconds
 * Returned 2 rows *
 
>>> df = db.dfquery("select * from working.seths_temp_test_table;")
>>> df.columns

Index([u'dta', u'other_field', u'typ'], dtype='object')

>>> df

   dta  other_field  typ
0    1            2  old
1    8            9  new

>>> df.dta

0    1
1    8
Name: dta, dtype: int64

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


### print_last_query
**`DbConnect.print_last_query()`**

Prints latest query run with basic formatting. 
###### Parameters:
 - None
**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("""
    select n.nodeid, street
    from node n
    join (
        select nodeidfrom nodeid, street from lion
        union
        select nodeidto nodeid, street from lion
    ) l
    on n.nodeid=l.nodeid::int
    limit 5
""")

- Query run 2021-08-05 10:39:00.759000
 Query time: Query run in 123000 microseconds
 * Returned 5 rows *
 
>>> db.print_last_query()

    select n.nodeid, street
    from node n
    join (
        select nodeidfrom nodeid, street from lion
        union
        select nodeidto nodeid, street from lion
    ) l
    on n.nodeid=l.nodeid::int
    limit 5

>>>

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


### dataframe_to_table_schema
**`DbConnect.dataframe_to_table_schema(df, table, schema=None, overwrite=False, temp=True, allow_max_varchar=False,
                                  column_type_overrides=None, days=7)`**

Translates Pandas `DataFrame` into empty database table. Generates an empty database table using the column names and panda's datatype inferences.
Returns table schema that was created from `DataFrame`.
 
###### Parameters:
 - **`df` DataFrame**: Pandas `DataFrame` to be added to database
 - **`table` str**: Table name to be used in the database
 - **`schema` str, default None**: Database schema to use for destination in database (defaults database object's default schema)
 - **`overwrite` bool, default False**: If table exists in database will overwrite if True (defaults to `False`)
 - **`temp` bool, default True**: Optional flag to make table as not-temporary (defaults to `True`)
 - **`allow_max_varchar` bool, default False**: Boolean to allow unlimited/max varchar columns; defaults to `False`
 - **`column_type_overrides` Dict, default None'**: Dict of type {key=column name, value=column type}. Will manually set the
                raw column name as that type in the query, regardless of the pandas/postgres/sql server automatic
                detection.
 - **`days` int, default 7**: Defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted  
 
**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> df = db.dfquery("select 1 as int_col, 'text' as text_col, now() as timstamp_col;")
 
>>> db.dataframe_to_table_schema(df, 'seths_temp_test_table', schema='working', overwrite=True)
[['int_col', 'bigint'], ['text_col', 'varchar (500)'], ['timstamp_col', 'varchar (500)']]

>>> db.dfquery("select * from working.seths_temp_test_table")

Empty DataFrame
Columns: [int_col, text_col, timstamp_col]
Index: []

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


### dataframe_to_table
**`DbConnect.dataframe_to_table(df, table, table_schema=None, schema=None, overwrite=False, temp=True,
                           allow_max_varchar=False, column_type_overrides=None, days=7)`**

Translates Pandas `DataFrame` into populated database table. This uses dataframe_to_table_schema to generate an empty database table 
and then inserts the dataframe's data into it. 
 
###### Parameters:
 - **`df` DataFrame**: Pandas `DataFrame` to be added to database
 - **`table` str**: Table name to be used in the database
 - **`table_schema` list, default None**:  schema of `DataFrame` (returned from `dataframe_to_table_schema`)
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`overwrite` bool, default False**: If table exists in database will overwrite if `True` (defaults to `False`)
 - **`temp` bool, default True**: Optional flag to make table as not-temporary (defaults to `True`)
 - **`allow_max_varchar` bool, default False**: Boolean to allow unlimited/max `varchar` columns; defaults to `False`
 - **`column_type_overrides` Dict, default None'**: Dict of type {key=column name, value=column type}. Will manually set the
                raw column name as that type in the query, regardless of the pandas/postgres/sql server automatic
                detection.
 - **`days` int, default 7**: Defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted  
 
**Sample**


```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> df = db.dfquery("select 1 as int_col, 'text' as text_col, now() as timstamp_col;")
 
>>> db.dataframe_to_table(df, 'seths_temp_test_table', schema='working', overwrite=True)

Reading data into Database

1it [00:00, 50.00it/s]

1 rows added to working.seths_temp_test_table

>>> db.dfquery("select * from working.seths_temp_test_table")

   int_col text_col      timstamp_col
0        1     text  2021-08-06 13:27

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


#### csv_to_table

**`DbConnect.csv_to_table(input_file=None, overwrite=False, schema=None, table=None, temp=True, sep=',',
                     long_varchar_check=False, column_type_overrides=None, days=7)`**

Imports csv file to database. This uses pandas datatypes to generate the table schema.
###### Parameters:
 - **`input_file` DataFrame, default None**: File path to csv file; if None, prompts user input
 - **`overwrite` bool, default False**: If table exists in database will overwrite if `True` (defaults to `False`)
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`table` str, default None**: Name for final database table; if None will use file name in input_file's path 
 - **`temp` bool, default True**: Optional flag to make table as not-temporary (defaults to `True`)
 - **`sep` str, default ','**: Separator for csv file, defaults to comma (,)
 - **`long_varchar_check` bool, default False**: Boolean to allow unlimited/max varchar columns; defaults to `False`
 - **`column_type_overrides` Dict, default None'**: Dict of type {key=`column name`, value=`column type`}. Will manually set the
                raw column name as that type in the query, regardless of the pandas/postgres/sql server automatic
                detection. This will not override a custom table_schema (if provided)
 - **`days` int, default 7**: If temp=`True`, defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted.
 
**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> df = db.dfquery("select 1 as int_col, 'text' as text_col, now() as timstamp_col;")
>>> df.to_csv('seths_sample_file.csv')
>>> db.csv_to_table('seths_sample_file.csv', schema='working')
 
Reading data into Database

1it [00:00, 58.82it/s]

1 rows added to working.seths_sample_file
 
>>> db.dfquery("select * from working.seths_sample_file")

  unnamed__0  int_col text_col                      timstamp_col
0           0        1     text  2021-08-06 13:36:10.821789-04:00
```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


#### xls_to_table
**`DbConnect.xls_to_table(input_file=None, sheet_name=0, overwrite=False, schema=None, table=None, temp=True,
                     column_type_overrides=None, days=7)`**

Imports xls file to database. This uses pandas datatypes to generate the table schema.
###### Parameters:
 - **`input_file` DataFrame, default None**: File path to excel file; if `None`, prompts user input
 - **`sheet_name` str, int, or None, default 0**: Name or ordinal position of excel sheet/tab to import. If none provided it will default to the 1st sheet
 - **`overwrite` bool, default False**: If table exists in database will overwrite if True (defaults to `False`)
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`table` str, default None**: Table name to be used in the database; if None will use file name in input_file's path 
 - **`temp` bool, default True**: Optional flag to make table as not-temporary (defaults to `True`)
 - **`column_type_overrides` Dict, default None'**: Dict of type {key=`column name`, value=`column type`}. Will manually set the
                raw column name as that type in the query, regardless of the pandas/postgres/sql server automatic
                detection.
 - **`days` int, default 7**: Defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted  
 
**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> df = db.dfquery("select 1 as int_col, 'text' as text_col, now()::date as timstamp_col;")
>>> df.to_excel('seths_sample_file.xlsx')
>>> db.xls_to_table('seths_sample_file.xlsx', schema='working')

working.seths_sample_file already exists. Use overwrite=True to replace.

>>> db.xls_to_table('seths_sample_file.xlsx', schema='working', overwrite=True)

Bulk loading data...


            1 rows added to working.stg_seths_sample_file.
            The table name may include stg_. This will not change the end result.

- Query run 2021-08-09 10:59:01.520000
 Query time: Query run in 5000 microseconds
 * Returned 0 rows *
  
Reading data into Database

1it [00:00, 58.82it/s]

1 rows added to working.seths_sample_file
 
>>> db.dfquery("select * from working.seths_sample_file")

   ogc_fid  field1  int_col text_col timstamp_col
0        1       0        1     text   2021-08-09
```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


#### query_to_csv
**`DbConnect.query_to_csv(query, strict=True, output_file=None, open_file=False, sep=',', quote_strings=True,
                     quiet=False)`**
Exports query results to a csv file. 

###### Parameters:
 - **`query` str**: SQL query as string type; the query should ultimately return data (ie. include a `select` statement) 
 - **`strict` bool, default True**: If `True` will run `sys.exit` on failed query attempts
 - **`output_file` str, default None**: File path for resulting csv file, if not provided the output will write a file to current directory named `data_[YYYMMDD].csv`
 - **`open_file` bool, default False**:  If `True` output file will be automatically opened when complete 
 - **`sep` str, default `,`**: Delimiter for csv; defaults to comma (,) 
 - **`quote_strings` bool, default True**: Defaults to `True` (`csv.QUOTE_ALL`); if False, will `csv.QUOTE_MINIMAL`
 - **`quiet` bool, default False'**: If `True` will override default behavior which outputs query metrics and output location

**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query_to_csv("select street, segmentid, lboro from lion limit 25;")

- Query run 2021-08-09 13:34:11.942000
 Query time: Query run in 18000 microseconds
 * Returned 25 rows *
Writing to C:\Users\seth\data_202108091334.csv

>>> db.query_to_csv("select street, segmentid, lboro from lion limit 25;", output_file= r'E:\RIS\Staff Folders\Seth\sample\seth_sample_data.csv', open_file=True)
- Query run 2021-08-09 13:35:20.986000
 Query time: Query run in 2000 microseconds
 * Returned 25 rows *
Writing to E:\RIS\Staff Folders\Seth\sample\seth_sample_data.csv

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


#### query_to_map
**`DbConnect.query_to_map(query, value_column, geom_column=None, id_column=None)`**

Generates simple Plotly Choropleth Map from query results. 
If no geom_column is specified, and the results contain columns named `precinct`, `nta`, `ntacode`, `boro`, `borough`, 
or `borocode`, it will automatically link to precinct, NTA, or borough, respectively. **This will only work if the database connected to contains the appropriate tables:**
- districts_police_precincts
- districts_neighborhood_tabulation_areas
- districts_boroughs

###### Parameters:
 - **`query` str**: SQL query as string type; the query should ultimatley return data (ie. include a `select` statement with polygon geometry or must contain appropriate join attrbute) 
 - **`value_column` str**: The name of column with the value that is being mapped
 - **`geom_column` str, default None**: the column with the geom that is being mapped;
            if not filled in, columns must contain `precinct`, `nta`, `ntacode`, `boro`, `borough`, or `borocode`
            *Must be used in conjunction with an id_column*
 - **`id_column` str, default False**: The name of the column that contains the ID of the geography being mapped (ex. precinct, nta, boro);
            if not filled in, columns must contain `precinct`, `nta`, `ntacode`, `boro`, `borough`, or `borocode`
            *Must be used in conjunction with an geom_column*

**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query_to_map("""
select 
    lntacode as nta, 
    count(*) cnt, 
    n.geom 
from lion l 
join districts_neighborhood_tabulation_areas n 
    on l.lntacode=n.ntacode 
group by 
    lntacode, n.geom
""", 'cnt', id_column='nta', geom_column='geom')
```
Rely on on geom from districts table 
```
>>> import pysqldb3
>>> db = pysqldb.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query_to_map("select lntacode as nta, count(*) cnt from lion group by lntacode;", 'cnt')

```


![alt text](https://github.com/safety-analytics-mapping/ris/blob/docs/Capture.JPG?raw=true)

[Back to Table of Contents](#pysqldb-public-functions)
<br>





#### query_to_shp
**`DbConnect.query_to_shp(query, path=None, shp_name=None, cmd=None, gdal_data_loc=GDAL_DATA_LOC,
                     print_cmd=False, srid=2263)`**

Generates shapefile output from the data returned from a query. 

###### Parameters:
 - **`query` str**: SQL query as string type; the query should ultimatley return data (ie. include a `select` statement with polygon geometry or must contain appropriate join attrbute) 
 - **`shp_name` str, default None**: Output filename to be used for shapefile (should end in `.shp`)
 - **`path` str, default None**: Folder path where the output shapefile will be written to, if none provided user input is required
 - **`cmd` str, default None**: GDAL command to overwrite default behavior 
 - **`gdal_data_loc` str, default None**: Path to gdal data, if not stored in system env correctly
 - **`print_cmd` str, default None**: Option to print `ogr` command (without password)
 - **`srid` int, default 2263**: SRID to manually set output to.

**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query_to_shp("select street, segmentid, geom from lion where street ='WATER STREET'", path=r'E:\RIS\Staff Folders\Seth\sample', shp_name='sample_shp.shp', print_cmd=True)

- Query run 2021-08-09 17:04:43.135000
 Query time: Query run in 116000 microseconds
 * Returned 0 rows *
 ogr2ogr -overwrite -f "ESRI Shapefile" "E:\RIS\Staff Folders\Seth\sample\sample_shp.shp" PG:"host=dotdevrhpgsql01 user=shostetter dbname=ris password=**************" -sql "SELECT * FROM (select \"geom\" , \"segmentid\" , \"street\" from (select street, segmentid, geom from lion where street ='WATER STREET') q ) x"

sample_shp.shp shapefile
written to: E:\RIS\Staff Folders\Seth\sample
generated from: select \"geom\" , \"segmentid\" , \"street\" from (select street, segmentid, geom from lion where street ='WATER STREET') q
- Query run 2021-08-09 17:04:45.027000
 Query time: Query run in 8000 microseconds
 * Returned 0 rows *

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>



#### table_to_shp
**`DbConnect.table_to_shp(table, schema=None, strict=True, path=None, shp_name=None, cmd=None,
                     gdal_data_loc=GDAL_DATA_LOC, print_cmd=False)`**

Generates shapefile ouput from the data returned from a query. 

###### Parameters:
 - **`table` str**: SQL query as string type; the query should ultimatley return data (ie. include a `select` statement with polygon geometry or must contain appropriate join attrbute) 
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`shp_name` str, default None**: Output filename to be used for shapefile (should end in `.shp`)
 - **`strict` bool, default True**: If True will run `sys.exit` on failed query attempts
 - **`path` str, default None**: Folder path where the output shapefile will be written to, if none provided user input is required
 - **`cmd` str, default None**: GDAL command to overwrite default behavior 
 - **`gdal_data_loc` str, default None**: Path to gdal data, if not stored in system env correctly
 - **`print_cmd` str, default None**: Option to print `ogr` command (without password)
 - **`srid` int, default 2263**: SRID to manually set output to

**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("create table working.sample as select segmentid, number_travel_lanes, corridor_street, carto_display_level, created, geom from lion")
 
 - Query run 2021-08-10 10:11:13.615000
 Query time: Query run in 720000 microseconds
 * Returned 0 rows *
 
>>> db.table_to_shp('sample', schema='working', path=r'E:\RIS\Staff Folders\Seth\sample', shp_name='lion_sample_shp.shp')
 
- Query run 2021-08-10 10:12:23.264000
 Query time: Query run in 6000 microseconds
 * Returned 0 rows *

            The following columns are of type datetime/timestamp:

            ['created']

            Shapefiles don't support datetime/timestamps with both the date and time. Each column will be split up
            into colname_dt (of type date) and colname_tm (of type **string/varchar**).

Warning 6: Normalized/laundered field name: 'number_travel_lanes' to 'number_tra'
Warning 6: Normalized/laundered field name: 'carto_display_level' to 'carto_disp'
Warning 6: Normalized/laundered field name: 'corridor_street' to 'corridor_s'

lion_sample_shp.shp shapefile
written to: E:\RIS\Staff Folders\Seth H\Misc
generated from: select \"geom\" , \"number_travel_lanes\" , \"carto_display_level\" , \"corridor_street\" , \"segmentid\" , cast(\"created\" as date) \"created_dt\", cast(cast(\"created\" as time) as varchar) \"created_tm\"  from (select * from working.sample) q
- Query run 2021-08-10 10:12:50.677000
 Query time: Query run in 2000 microseconds
 * Returned 0 rows *

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>



#### table_to_csv
**`DbConnect.table_to_csv(table, schema=None, strict=True, output_file=None, open_file=False, sep=',',
                     quote_strings=True)`**

Generates shapefile ouput from the data returned from a query. 

###### Parameters:
 - **`table` str**: Name of database table to be used  
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`strict` bool, default True**: If True will run sys.exit on failed query attempts
 - **`output_file` str, default None**: String for csv output file location and file name. If none provided defaults to current directory and table name
 - **`open_file` bool, default False**: Option to automatically open output file when finished; defaults to False
 - **`sep` str, default ','**: Seperator to use for csv (defaults to `,`) 
 - **`quote_strings` bool, default True**: Boolean flag for adding quote strings to output (defaults to true, QUOTE_ALL)

**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.query("create table working.sample as select segmentid, number_travel_lanes, corridor_street, carto_display_level, created, geom from lion")
 
 - Query run 2021-08-10 10:11:13.615000
 Query time: Query run in 720000 microseconds
 * Returned 0 rows *
 
>>> db.table_to_csv('sample', schema='working', output_file=r'E:\RIS\Staff Folders\Seth\sample\lion_sample_shp.csv'')

 - Query run 2021-08-10 10:41:26.242000
 Query time: Query run in 2000 microseconds
 * Returned 0 rows *
Writing to E:\RIS\Staff Folders\Seth\sample\lion_sample_shp.csv

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>



#### shp_to_table

**`DbConnect.shp_to_table(path=None, table=None, schema=None, shp_name=None, cmd=None,
                     port=None, gdal_data_loc=GDAL_DATA_LOC, precision=False, private=False, temp=True,
                     shp_encoding=None, print_cmd=False, days=7)`**

Imports ESRI Shapefile to database, uses GDAL to generate the table.

###### Parameters:
 - **`path` str, default None**: File path of the shapefile; if None, prompts user input
 - **`table` str, default None**: Table name to be used in the database; if None will use shapefile's name 
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`shp_name` str, default None**: Output filename to be used for shapefile (should end in .shp)
 - **`cmd` str, default None**: optional ogr2ogr command to overwrite default
 - **`srid` int, default 2263**: SRID to use 
 - **`port` str, default None**:  Database port to use, defaults database connection port
 - **`gdal_data_loc` str, default None**: Path to gdal data, if not stored in system env correctly
 - **`precision` bool, default False**:  Sets precision flag in ogr (defaults to `-lco precision=NO`)
 - **`private` bool, default False**: Flag for permissions output table in database (Defaults to False - will grant select to public)
 - **`temp` bool, default True**: Optional flag to make table as not-temporary (defaults to True)
 - **`shp_encoding` str, default None**: If not None, sets the PG client encoding while uploading the shpfile. Options inlude `LATIN1` or `UTF-8`.
 - **`print_cmd` str, default None**: Option to print ogr command (without password)
 - **`days` int, default 7**: if temp=True, number of days that the temp table will be kept
 
**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.shp_to_table(path=r'E:\RIS\Staff Folders\Seth\sample', shp_name='lion_sample_shp.shp', table='lion_sample_import', schema='working')

0...10...20...30...40...50...60...70...80...90...100 - done.

- Query run 2021-08-10 11:03:26.298000
 Query time: Query run in 55000 microseconds
 * Returned 0 rows *

>>> db.dfquery("select * from working.lion_sample_import limit 3")
   ogc_fid number_tra  ...    created_tm                                               geom
0        1       None  ...  13:11:10.962  0105000020D70800000100000001020000000200000000...
1        2       None  ...  13:11:10.962  0105000020D70800000100000001020000000200000000...
2        3       None  ...  13:11:10.962  0105000020D70800000100000001020000000200000080...

[3 rows x 8 columns]

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>



#### feature_class_to_table

**`DbConnect.feature_class_to_table(path, table, schema=None, shp_name=None, gdal_data_loc=GDAL_DATA_LOC, srid=2263,
                               private=False, temp=True, fc_encoding=None, print_cmd=False,
                               days=7)`**

Imports featureclass from ESRI file geodatabase, uses GDAL to generate the table.

###### Parameters:
 - **`path` str**: File path of the geodatabase
 - **`table` str**: Table name to be used in the database
 - **`schema` str, default None**:  Database schema to use for destination in database (defaults database object's default schema)
 - **`shp_name` str, default None**: Output filename to be used for shapefile
 - **`gdal_data_loc` str, default None**: Path to gdal data, if not stored in system env correctly
 - **`srid` int, default 2263**: SRID to use
 - **`private` bool, default False**: Flag for permissions output table in database (Defaults to False - will grant select to public)
 - **`temp` bool, default True**: Optional flag to make table as not-temporary (defaults to True)
 - **`fc_encoding` str, default None**: If not `None`, sets the PG client encoding while uploading the shpfile. Options inlude `LATIN1` or `UTF-8`.
 - **`print_cmd` str, default None**: Option to print ogr command (without password)
 - **`days` int, default 7**: Defines the lifespan (number of days) of any tables created in the query, before they are automatically deleted  
  
 
**Sample**

```
>>> import pysqldb3
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> db.feature_class_to_table(path=r'E:\RIS\Staff Folders\Seth\sample\file_geodatabase.gdb', shp_name='Pct81', table='sample_fc_import', schema='working')

, table='sample_fc_import', schema='working')
0...10...20...30...40...50...60...70...80...90...100 - done.

- Query run 2021-08-10 11:22:34.254000
 Query time: Query run in 2000 microseconds
 * Returned 0 rows *
 
>>> db.dfquery("select * from working.sample_fc_import limit 3")
   objectid_1  objectid  loc  ...             x              y                                               geom
0           1     12495  INT  ...  1.001274e+06  186245.989763  0104000020D70800000100000001010000000045FD8F73...
1           2     12496  INT  ...  1.001306e+06  186672.914762  0104000020D70800000100000001010000008080F1B8B3...
2           3     12497  INT  ...  1.001326e+06  186946.733112  0104000020D708000001000000010100000000A8ED4EDB...

[3 rows x 16 columns]

```

[Back to Table of Contents](#pysqldb-public-functions)
<br>


## 2. Query - query.py 

query contains `Query`, a class built to support the query interactions of `Pysql.DbConnect`. The `Query` Class can operate independently, but requires a `DbConnection` instance. The majority of the functionality is intended to be accessed via `DbConnect`.
 
### 2.1 Simple Example/Setup  
To create a DbConnect object:
1. Import `import pysqldb3, query`
2. `db = pysqldb.DbConnect(type='PG', server='server_name', database='db_name')` 
    + Replace `server_name` and `db_name` with the actual values. 
    + You must specify the type, either `PG` (Postgres) or `MS` (SQL Server). 
    + You can also add your username using `user='my_username'` 
    + You can add your password similarly using `password='mypassword'`
    + Other inputs include LDAP and ports. If you're unsure about these, feel free to ask around. 
3. `qry = query.Query(db, 'select * from my_schema.my_table')` this is equivalent to using `db.query('select * from my_schema.my_table')`


### 1.2 Functions 
In Jupyter or Python shell, use `help(pysqldb)` to show all public functions and their inputs. <br>
#### pysqldb public functions:
1. [`dfquery`](#dfquery2): Runs from input SQL string, called from `DbConnnect` with `return_df=True`; returns Pandas `DataFrame`.
1. [`query_creates_table`](#query_creates_table): Checks if query generates new tables, static method.
1. [`query_drops_table`](#query_drops_table): Checks if query drops tables, static method.
1. [`query_renames_table`](#query_renames_table): Checks if query renames tables, static method.
1. [`rename_index`](#rename_index): Renames any indexes associated with a table. Used when a table is renamed to keep the indexes up to date.
1. [`query_to_csv`](#query_to_csv): Writes results of the query to a csv file, called from `DbConnnect`.
1. [`query_to_shp`](#query_to_shp): Writes results of the query to a shapefile by calling `Shapefile` `ogr` command in `write_shp` function, called from `DbConnnect`.
1. [`print_query`](#print_query): Prints query string with basic formatting, static method.



## Details 
### dfquery
**`query.dfquery()`**

Returns data from query as a Pandas `DataFrame`
###### Parameters:
 - None
  
**Sample**

Use query to set up sample table and dfquery to explore results in pandas.
```
>>> import pysqldb3, query
>>> db = pysqldb3.DbConnect(type='pg', server=server_address, database='ris', user='shostetter', password='*******')
>>> qry=query.Query(dbo, 'select * from my_schema.my_table')

db.query("create table working.seths_temp_test_table as select 1 as dta, 2 as other_field")

- Query run 2021-08-04 16:09:25.171000
 Query time: Query run in 36000 microseconds
 * Returned 0 rows *
 
 >>> db.tables_created

['working.seths_temp_test_table']
```

Basic select query and verify that the results are stored in the `data` attribute
```
>>> db.query("select * from working.seths_temp_test_table")

- Query run 2021-08-04 16:10:56.926000
 Query time: Query run in 2000 microseconds
 * Returned 1 rows *
 
>>> db.data

[(1, 2)]
```

Multiple queries tied together 
```
>>> db.query("""
    drop table if exists working.seths_temp_test_table; 
    create table working.seths_temp_test_table as select 1 as dta, 2 as other_field;
    alter table working.seths_temp_test_table add column typ varchar;
    update working.seths_temp_test_table set typ = 'old';
    insert into working.seths_temp_test_table values (8, 9, 'new');
    select typ, count(*) as cnt from working.seths_temp_test_table   group by typ;
""")

- Query run 2021-08-04 16:46:18.539000
 Query time: Query run in 23000 microseconds
 * Returned 2 rows *

>>> db.data

[('old', 1L), ('new', 1L)]
```

Failed query in non-strict mode
```
>>> db.query("drop table working.seths_temp_test_table; select * from working.seths_temp_test_table", strict=False)

- Query failed: relation "working.seths_temp_test_table" does not exist
LINE 1: ...able working.seths_temp_test_table; select * from working.se...

- Query run 2021-08-04 16:19:45.485000
        drop table working.seths_temp_test_table; select * from working.seths_temp_test_table

```
[Back to Table of Contents](#pysqldb-public-functions)
<br>
############################## TODO ####################################################
## 3. Shapefile - shapefile.py 

#### pysqldb public functions:
1. [`name_extension`](#name_extension): Adds `.shp` extension to provided filename.
1. [`write_shp`](#write_shp): Write out a shapefile from current database.
1. ['table_exists`](#table_exists_2): Wrapper for `DbConnect` `table_exists` method.
1. ['del_indexes`](#del_indexes): Drops indexes from database object.
1. ['read_shp'](#read_shp): Read in a shapefile as a table.
1. ['read_feature_class'](#read_feature_class): Read in a feature class of a shapefile as a table.
1. ['rename_geom'](#rename_geom): Renames `wkb_geometry` column in table to `geom`, along with index.


#### name_extension
**`DbConnect.shapefile.name_extension(self, name)`**
Adds `.shp` to the provided filename, if not already there.
###### Parameters:
- **name: string, default None**: The filename to append `.shp` to.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### write_shp
**`DbConnect.shapefile.write_shp(self, print_cmd=False)`**
Creates and writes a shapefile from the database using GDAL.
###### Parameters:
- **print_cmd: bool, default False**: Optional flag to print the GDAL command being used.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### table_exists
**`DbConnect.shapefile.table_exists(self)`**
Wrapper for DbConnect `table_exists` method.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### del_indexes
**`DbConnect.shapefile.del_indexes(self)`**
Drops indexes in this database object.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### read_shp
**`DbConnect.shapefile.read_shp(self, precision=False, private=False,shp_encoding=None, print_cmd=False)`**
Reads in a shapefile as a table.
###### Parameters:
- **`precision`: bool, default False**
- **`private`: bool, default False**
- **`shp_encoding`: str, default None**: Encoding of data within shapefile
- **`print_cmd`: bool, default False**: Optional flag to print the GDAL command that is being used.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### read_feature_class
**`DbConnect.shapefile.read_feature_class(self, private=False, print_cmd=False, fc_encoding=None)`**
Read in a feature class of a shapefile as a table.

###### Parameters:
- **`private`: bool, default False**
- **`print_cmd`: bool, default False**: Optional flag to print the GDAL command being used.
- **`fc_encoding`: string, default None**: Optional encoding of data within feature class.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### rename_geom
**`DbConnect.shapefile.rename_geom(self)`**
Renames `wkb_geometry` column to `geom`, along with index.

[Back to Table of Contents](#pysqldb-public-functions)
<br>


## 4. Data IO - data_io.py 

#### pysqldb public functions:
1. ['pg_to_sql'](#pg_to_sql): Migrates tables from PostgreSQL to MS SQL Server. Also generates spatial tables in MSSQLS if present in pgSQL.
1. ['sql_to_pg_qry'](#sql_to_pg_qry): Migrates the result of a query from MS SQL Server to PostgreSQL. Also generates spatial tables in pgSQL if present in MSSQLS.
1. ['sql_to_pg'](#sql_to_pg): Migrates tables from MS SQL Server to PostgreSQL. Also generates spatial tables in pgSQL if present in MSSQLS.
1. ['pg_to_pg'](#pg_to_pg): Migrates tables from an existing PostgreSQL database to another PostgreSQL database.

#### pg_to_sql
**`DbConnect.data_io.pg_to_sql(pg, ms, org_table, LDAP=False, spatial=True, org_schema=None, dest_schema=None, dest_print_cmd=False, temp=True)`**
Migrates tables from PostgreSQL to MS SQL Server database, and generates spatial tables in output MS SQL Server database if they exist in PostgreSQL.
###### Parameters:
- **`pg`: DbConnect**: DbConnect instance connecting to PostgreSQL source database.
- **`ms`: DbConnect**: DbConnect instance connecting to MS SQL Server destination database.
- **`org_table`: str**: Table name of table to migrate.
- **`LDAP`: bool, default False**: Whether to use LDAP credentials when connecting to databases.
- **`spatial`: bool, default True**: Flag for spatial table
- **`org_schema`: schema**: PostgreSQL Schema for origin table. Defaults to original db's default schema.
- **`dest_schema`: schema**: MS SQL Server Schema for destination table. Defaults to destination db's default schema.
- **`print_cmd`: bool, default False**: Option to print the `ogr2ogr` command-line statement for debug purposes.
- **`temp`: bool, default True**: Flag for temporary table.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### sql_to_pg_qry
**`DbConnect.data_io.sql_to_pg_qry(ms, pg, query, LDAP=false, spatial=True, dest_schema=None, print_cmd=False, temp=True, dest_table=None)`**
Migrates the result of a query from MS SQL Server database to PostgreSQL, and generates spatial tables in output PostgreSQL database if they exist in MS SQL Server.
###### Parameters:
- **`pg`: DbConnect**: DbConnect instance connecting to PostgreSQL source database.
- **`ms`: DbConnect**: DbConnect instance connecting to MS SQL Server destination database.
- **`query`: str**: SQL Query to run on MS SQL Server database. Its results will be output as PostgreSQL.
- **`LDAP`: bool, default False**: Whether to use LDAP credentials when connecting to databases.
- **`spatial`: bool, default True**: Flag for spatial table
- **`dest_table`: str**: Destination table name
- **`dest_schema`: schema**: MS SQL Server Schema for destination table. Defaults to destination db's default schema.
- **`print_cmd`: bool, default False**: Option to print the ogr2ogr command-line statement for debug purposes.
- **`temp`: bool, default True**: Flag for temporary table.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### sql_to_pg
**`DbConnect.data_io.sql_to_pg(ms, pg, org_table, LDAP=False, spatial=True, org_schema=None, dest_schema=None, print_cmd=False, dest_table=None, temp=True, gdal_data_loc=GDAL_DATA_LOC, pg_encoding='UTF8')`**
Migrates tables from MS SQL Server Database to PostgreSQL, and generates spatial tables in output postgreSQL database if they exist in MS SQL Server.
###### Parameters:
- **`pg`: DbConnect**: DbConnect instance connecting to PostgreSQL source database.
- **`ms`: DbConnect**: DbConnect instance connecting to MS SQL Server destination database.
- **`org_table`: str**: Table name of table to migrate.
- **`LDAP`: bool, default False**: Whether to use LDAP credentials when connecting to databases.
- **`spatial`: bool, default True**: Flag for spatial table
- **`org_schema`: schema**: PostgreSQL Schema for origin table. Defaults to original db's default schema.
- **`dest_schema`: schema**: MS SQL Server Schema for destination table. Defaults to destination db's default schema.
- **`print_cmd`: bool, default False**: Option to print the `ogr2ogr` command-line statement for debug purposes.
- **`temp`: bool, default True**: Flag for temporary table.
- **`gdal_data_loc`: str, default GDAL_DATA_LOC** Location of GDAL data if not set in environment variable.
- **`pg_encoding`: str, default UTF8**: Encoding to use for PostgreSQL client.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### pg_to_pg
**`DbConnect.data_io.pg_to_pg(from_pg, to_pg, org_table, org_schema=None, dest_schema=None, print_cmd=False, dest_table=None, spatial=True, temp=True)`**
Migrates tables from one PostgreSQL database to another PostgreSQL database.
###### Parameters:
- **`from_pg`: DbConnect**: `DbConnect` object corresponding to source pgSQL database.
- **`to_pg`: DbConnect**: `DbConnect` object corresponding to destination pgSQL database.
- **`org_table`: str**: Table name of table to migrate.
- **`org_schema`: schema**: PostgreSQL Schema for origin table. Defaults to original db's default schema.
- **`dest_schema`: schema**: MS SQL Server Schema for destination table. Defaults to destination db's default schema.
- **`dest_table`: str, default None**: New name for destination table. If `None`, will use name of original table.
- **`spatial`: bool, default True**: Flag for spatial table
- **`print_cmd`: bool, default False**: Option to print the `ogr2ogr` command-line statement for debug purposes.
- **`temp`: bool, default True**: Flag for temporary table.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

### 4.1 Example 
## 5. Geocoder - Geocoder.py 
## 6. Reverse Geocoder - ReverseGeocoder.py 
## 7. MV104s - get_mv104s.py 
## 8. Helper Files 
### 8.1. SQL Queries - sql.py 
+ Contains large SQL queries used in this library 
### 9.2 Command Line Prompts - cmds.py 
+ Contains large/complicated command line prompts, normally using gdal
### 9.3 Utility Functions - util.py 
+ Contains small functions used by the various classes.

#### pysqldb public functions:
['clean_query_special_characters'](#clean_query_special_characters): Cleans special characters from an SQL query.
['clean_geom_column'](#clean_geom_column): Checks for a column named `wkb_geometry` and renames it to `geom`.
['get_unique_table_schema_string'](#get_unique_table_schema_string): Takes a raw input for a pgSQL/MSSQLS table and distills the name in the way it is stored in the database.
['get_query_table_schema_name'](#get_query_table_schema_name): Takes a cleaned input from the log table and makes changes to ensure it is interpreted correctly by pgSQL/MSSQLS.
['parse_table_string'](#parse_table_string): Parses and extracts the schema and table names from table references in query strings.
['type_decoder'](#type_decoder): Lazy type decoding from pandas to SQL.
['clean_cell'](#clean_cell): Formats CSV cells for SQL to add to database.
['clean_column'](#clean_column): Reformats column names for pgSQL/MSSQLS database.
['convert_geom_col'](#convert_geom_col): TBD
['clean_df_before_output'](#clean_df_before_output): Aggregate all data-cleaning operations to be performed on pandas `DataFrames` before they're applied.
['file_loc'](#file_loc): Opens a file picker.
['parse_shp_path'](#parse_shp_path): Parse and extract the shapefile name from provided filepath.

#### clean_query_special_characters
**`DbConnect.utils.clean_query_special_characters(query_string)`**
Cleans special characters from the provided query string.
###### Parameters:
- **`query_string`: str**: The SQL query to clean special characters from.
###### Returns:
Cleaned query string.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### clean_geom_column
**`DbConnect.utils.clean_geom_column(db, table, schema)`**
Checks for a column named `wkb_geometry` and renames it to `geom`.
###### Parameters:
- **`db`: DbConnect**: `DbConnect` object to check for `wkb_geometry` column
- **`table`: str**: table name
- **`schema`: str**: database schema name
###### Returns:
Table with `wkb_geometry` columns renamed to `geom`

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### get_unique_table_schema_string
**`DbConnect.utils.get_unique_table_schema_string(tbl_str, db_type)`**
Takes a raw input for a pgSQL/MSSQLS table and distills the name in the way the database stores it. This allows for there to be one "cleaned" version for multiple variations of the same table, so they are not written into the log twice or erroneously *not* removed.

Ex. in pgSQL: `working.tbl`, `working.Tbl`, `working."tbl"` are all saved the same way by pgSQL.
Ex. in MSSQLS: `[dbo].[tbl]`, `[dbo]."tbl"`, `[dbo].tbl` are all saved the same way by MSSQLS.

###### Parameters:
- **`tbl_str`: str**: Table or schema string.
- **`db_type`: str**: Type of database.
###### Returns:
Unique table schema string.

[Back to Table of Contents](#pysqldb-public-functions)
<br>


#### get_query_table_schema_name
**`DbConnect.utils.get_query_table_schema_name(tbl_str, db_type)`**
The inverse of `get_unique_table_schema_string`. This takes a cleaned input from the log table and makes some minor changes to ensure pgSQL/MSSQLS interprets it correctly.

Ex. in pgSQL: if stored in log as `Table`, then must be queried as `"Table"` to ensure capital letter.
Ex. in MSSQLS: if stored in log as `"table"`, then must be queried as `["table"]` to ensure quotes.

###### Parameters:
- **`tbl_str`: str**: Table or schema string.
- **`db_type`: str**: Type of database.
###### Returns:
Table schema name.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### parse_table_string
**`DbConnect.utils.parse_table_string(tbl_str, default_schema, db_type)`**
Parses and extracts table name and schema from the provided table reference.
ex. `server.schema.table`, `schema.table`, `table`
###### Parameters:
- **`tbl_str`: str**: Table reference string
- **`default_schema`**: Default schema
- **`db_type`**: Database type (`PG` or `MS`)
###### Returns:
Schema name and table name, seperated by `.`

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### type_decoder
**`DbConnect.utils.type_decoder(typ, varchar_length=500)`**
Lazy type decoding from pandas to SQL. There are problems associated with `NaN` values for numeric types when stored as `Object` dtypes. This does not try to optimize for smallest-size dtype.
###### Parameters:
- **`typ`: np.dtype**: Numpy dtype for column
- **`varchar_length`: int, default 500**: Length of `varchar` columns
###### Returns:
String representing datatype.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### clean_cell
**`DbConnect.utils.clean_cell(x)`**
Formats CSV cells for addition to SQL database.
###### Parameters:
- **`x`**: Raw CSV cell value
###### Returns:
Formatted CSV cell value as python `Object`.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### clean_column
**`DbConnect.utils.clean_column(x)`**
Reformats column names for database.
###### Parameters:
- **`x`: str**: Column name
###### Returns:
Reformatted column name with special characters replaced.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### convert_geom_col
**`DbConnect.utils.convert_geom_col(df, geom_name="geom")`**
Converts `wkb_geometry` columns in Pandas `DataFrame` to specified name (default `geom`)
###### Parameters:
- **`df`: pd.DataFrame**: Pandas `DataFrame` with `wkb_geometry` column names to convert
- **`geom_name`: str, default 'geom'**: Column of `wkb_geometry` to be converted
###### Returns:
`DataFrame` with converted column names.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### clean_df_before_output
**`DbConnect.utils.clean_df_before_output(df, geom_name="geom")`**
Aggregate all data cleaning operations to be performed on pandas `DataFrame` before they're applied. This function does the following:
- Converts `wkb_geometry` columns to `geom`
- Converts unicode errors
###### Parameters:
- **`df`: pd.DataFrame** Pandas `DataFrame` with `wkb_geometry` names to convert
- **`geom_name`: str, default 'geom'**: Column of `wkb_geometry` to be converted
###### Returns:
`DataFrame` with converted column names.

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### file_loc
**`DbConnect.utils.file_loc(typ='file', print_message=None)`**
Open a tkinter file picker dialog to perform the operation specified in `typ` parameter.
###### Parameters:
- **`typ`: str, default 'file'**: The operation to perform with this file picker dialog. Options are `file`, `folder` and `save`.
- **`print_message`: str, default None**: for debug use

[Back to Table of Contents](#pysqldb-public-functions)
<br>

#### parse_shp_path
**`DbConnect.utils.parse_shp_path(path=None, shp_name=None)`**
Standardizes extracting shapefile name from path. If `shp_name` is provided, it will override anything in the path.
###### Parameters:
- **`path`: str, default None**: Path to folder containing shapefile
- **`shp_name`: str, default None**: Name of shapefile.
###### Returns
2-tuple of strings containing shapefile path and name

[Back to Table of Contents](#pysqldb-public-functions)
<br>

## 9. Testing 
 1. If not installed: 
 ```pip install pytest ```
 2. Go to ```ris/tests/```
 3. Add to `test_general.py` or create a new Python test filename using the naming convention `test_$NAME.py`. 
 4. Make a test function under the convention `def test_$FN_NAME()`
 5. The function should have assert statements that will fail if the code being tested does not perform as expected. 
 Example below.
 6. To test, go to ris directory on your terminal/command prompt and run ```pytest --vv```. 
 7. It will tell you which tests pass and which tests failed. 
 
#### 9.1 Example Test: 

We have a function in our code called: 
```
def squared(x):
    return x*x
 ```

In pytest test file, we make: 

```
import squared 

def test_squared(): 
    assert squared(6) == 36 
```

When Pytest runs, that test will fail if that assert statement does not match. 

 
