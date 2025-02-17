import os

import configparser

from .. import pysqldb3 as pysqldb

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "\\db_config.cfg")

db = pysqldb.DbConnect(type=config.get('PG_DB', 'TYPE'),
                       server=config.get('PG_DB', 'SERVER'),
                       database=config.get('PG_DB', 'DB_NAME'),
                       user=config.get('PG_DB', 'DB_USER'),
                       password=config.get('PG_DB', 'DB_PASSWORD'))

sql = pysqldb.DbConnect(type=config.get('SQL_DB', 'TYPE'),
                        server=config.get('SQL_DB', 'SERVER'),
                        database=config.get('SQL_DB', 'DB_NAME'),
                        ldap=True)

test_for_drop_table = 'test_for_drop_table_func_{}'.format(db.user)


class TestDropTablePG:
    def test_drop_table_basic(self):
        schema = 'working'
        query_string = """
        
        DROP TABLE IF EXISTS working.{};
        CREATE TABLE working.{} AS 
    
        SELECT 'a' as col1, 'b' as col2;
    
        """.format(test_for_drop_table, test_for_drop_table)

        db.query(query_string)
        db.drop_table(schema, test_for_drop_table)
        assert not db.table_exists(test_for_drop_table, schema=schema)

    def test_remove_table_from_log(self):
        query_string = """

        DROP TABLE IF EXISTS working.{};
        CREATE TABLE working.{} AS 

        SELECT 'a' as col1, 'b' as col2;

        INSERT INTO working.__temp_log_table_{}__ (tbl_id, table_owner,table_schema,table_name,created_on,expires) VALUES (0, '{}', 'working','{}','09/18/2020',null);

        """.format(test_for_drop_table, test_for_drop_table, db.user, db.user, test_for_drop_table)

        db.query(query_string)
        db.drop_table('working', test_for_drop_table)

        log_check_query_string = """
        
            SELECT tbl_id, table_owner, table_schema, table_name, created_on, expires
            FROM working.__temp_log_table_{}__
            WHERE table_name = '{}'
            
        """.format(db.user, test_for_drop_table)

        assert len(db.dfquery(log_check_query_string)) == 0

    def test_table_not_in_log(self):
        query_string = """
    
            DROP TABLE IF EXISTS working.{};
            CREATE TABLE working.{} AS 
    
            SELECT 'a' as col1, 'b' as col2;
            """.format(test_for_drop_table, test_for_drop_table)

        db.query(query_string)
        db.drop_table(schema='working', table=test_for_drop_table)

        log_check_query_string = """
        
            SELECT tbl_id, table_owner, table_schema, table_name, created_on, expires
            FROM working.__temp_log_table_{}__
            WHERE table_name = '{}'
        
        """.format(db.user, test_for_drop_table)

        assert len(db.dfquery(log_check_query_string)) == 0

    def test_table_DNE_but_in_log(self):
        query_string = """

        INSERT INTO working.__temp_log_table_{}__ (tbl_id, table_owner,table_schema,table_name,created_on,expires) VALUES (0, '{}', 'working','{}','09/18/2020',null);

        """.format(db.user, db.user, test_for_drop_table)

        db.query(query_string)
        db.drop_table('working', table=test_for_drop_table)

        log_check_query_string = """
            SELECT tbl_id, table_owner, table_schema, table_name, created_on, expires
            FROM working.__temp_log_table_{}__
            WHERE table_name = '{}'
        """.format(db.user, test_for_drop_table)

        assert len(db.dfquery(log_check_query_string)) == 0

    def test_table_does_not_exist(self):
        assert db.drop_table('working', test_for_drop_table) is None


class TestDropTableMS:

    def test_drop_table_basic(self):
        table_name = 'sql_test_table_{}'.format(sql.user)  # from helper.py

        schema = 'dbo'
        query_string = """

        IF OBJECT_ID('dbo.{0}', 'u') IS NOT NULL
        DROP TABLE dbo.{0};

        SELECT 'a' as col1, 'b' as col2
        INTO dbo.{0};

        """.format(test_for_drop_table)

        sql.query(query_string)
        sql.drop_table(schema, table=test_for_drop_table)

        assert not sql.table_exists(test_for_drop_table, schema=schema)

    def test_remove_table_from_log(self):
        table_name = 'sql_test_table_{}'.format(sql.user)  # from helper.py
        query_string = """

        IF OBJECT_ID('dbo.{dt}', 'u') IS NOT NULL
        DROP TABLE dbo.{dt};

        SELECT 'a' as col1, 'b' as col2
        INTO dbo.{dt};

        INSERT INTO [dbo].[__temp_log_table_{u}__] (table_owner,table_schema,table_name,created_on,expires) 
        VALUES ('{u}', 'dbo','{dt}','09/18/2020',null);

        """.format(dt=test_for_drop_table, u=sql.user)

        sql.query(query_string)
        sql.drop_table('dbo', table=test_for_drop_table)

        log_check_query_string = """
            SELECT tbl_id, table_owner, table_schema, table_name, created_on, expires
            FROM [dbo].[__temp_log_table_{}__]
            WHERE table_name = '{}'
        """.format(sql.user, test_for_drop_table)

        assert len(sql.dfquery(log_check_query_string)) == 0

    def test_table_not_in_log(self):
        table_name = 'sql_test_table_{}'.format(sql.user)  # from helper.py
        query_string = """

        IF OBJECT_ID('dbo.{t}', 'u') IS NOT NULL
        DROP TABLE dbo.{t};


        SELECT 'a' as col1, 'b' as col2
        INTO dbo.{t};

        """.format(t=test_for_drop_table)

        sql.query(query_string)
        sql.drop_table('dbo', table=test_for_drop_table)

        log_check_query_string = """
            SELECT tbl_id, table_owner, table_schema, table_name, created_on, expires
            FROM [dbo].[__temp_log_table_{}__]
            WHERE table_name = '{}'
        """.format(sql.user, test_for_drop_table)

        assert len(sql.dfquery(log_check_query_string)) == 0

    def test_table_DNE_but_in_log(self):
        query_string = """

        INSERT INTO [dbo].[__temp_log_table_{}__] (table_owner,table_schema,table_name,created_on,expires) 
        VALUES ('{}', 'dbo','{}','09/18/2020',null);

        """.format(sql.user, sql.user, test_for_drop_table)

        sql.query(query_string)
        sql.drop_table('dbo', table=test_for_drop_table)

        log_check_query_string = """
            SELECT tbl_id, table_owner, table_schema, table_name, created_on, expires
            FROM [dbo].[__temp_log_table_{}__]
            WHERE table_name = '{}'
        """.format(sql.user, test_for_drop_table)

        assert len(sql.dfquery(log_check_query_string)) == 0

    def test_table_does_not_exist(self):
        assert sql.drop_table('dbo', table=test_for_drop_table) is None
