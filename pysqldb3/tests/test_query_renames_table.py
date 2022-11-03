from .. import query

import os

import configparser

from .. import pysqldb3 as pysqldb

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "\\db_config.cfg")

db = pysqldb.DbConnect(type=config.get('PG_DB', 'TYPE'),
                       server=config.get('PG_DB', 'SERVER'),
                       port=int(config.get('PG_DB', 'PORT')),
                       database=config.get('PG_DB', 'DB_NAME'),
                       user=config.get('PG_DB', 'DB_USER'),
                       password=config.get('PG_DB', 'DB_PASSWORD'),
                       schema=config.get('PG_DB','DB_SCHEMA')
                       )

sql = pysqldb.DbConnect(type=config.get('SQL_DB', 'TYPE'),
                        server=config.get('SQL_DB', 'SERVER'),
                        database=config.get('SQL_DB', 'DB_NAME'),
                        user=config.get('SQL_DB', 'DB_USER'),
                        password=config.get('SQL_DB', 'DB_PASSWORD'),
                        schema=config.get('SQL_DB','DB_SCHEMA'),
                        ldap=True)

dspg = db.default_schema
dsms = sql.default_schema

class TestQueryCreatesTablesSql:
    def test_query_renames_table_from_qry(self):
        query_string = f"""
            EXEC sp_rename 'RISCRASHDATA.{dsms}.test_{sql.user}', 'node_{sql.user}'
        """
        assert query.Query.query_renames_table(query_string, dsms) == {f'{dsms}.node_{sql.user}': f'test_{sql.user}'}

    def test_query_renames_table_from_qry_no_db(self):
        query_string = f"""
             EXEC sp_rename '{dsms}.test_{sql.user}', 'node_{sql.user}'
         """
        assert query.Query.query_renames_table(query_string, dsms) == {f'{dsms}.node_{sql.user}': f'test_{sql.user}'}

    def test_query_renames_table_from_qry_just_table(self):
        query_string = f"""
             EXEC sp_rename 'test_{sql.user}', 'node_{sql.user}'
         """
        assert query.Query.query_renames_table(query_string, dsms) == {f'{dsms}.node_{sql.user}': f'test_{sql.user}'}

    def test_query_renames_table_from_qry_server(self):
        query_string = f"""
             EXEC sp_rename 'dotserver.RISCRASHDATA.{dsms}.test_{sql.user}', 'node_{sql.user}'
         """
        assert query.Query.query_renames_table(query_string, dsms) == {f'{dsms}.node_{sql.user}': f'test_{sql.user}'}

    def test_query_renames_table_from_qry_brackets(self):
        query_string = f"""
               EXEC sp_rename '[RISCRASHDATA].[{dsms}].[test_{sql.user}]', '[node_{sql.user}]'
           """
        assert query.Query.query_renames_table(query_string, default_schema=dsms) == {f'[{dsms}].[node_{sql.user}]': f'[test_{sql.user}]'}

    def test_query_renames_table_from_qry_multiple(self):

        query_string = f"""
            EXEC sp_rename 'RISCRASHDATA.{dsms}.test3_{sql.user}', 'node0_{sql.user}'

            select *
             into RISCRASHDATA.{dsms}.test_{sql.user}
            from RISCRASHDATA.{dsms}.test0_{sql.user};

            EXEC sp_rename 'RISCRASHDATA.{dsms}.test_{sql.user}', 'node_{sql.user}'
        """

        assert query.Query.query_renames_table(query_string, default_schema=dsms) == \
        {f"{dsms}.node_{sql.user}": f"test_{sql.user}", f"{dsms}.node0_{sql.user}": f"test3_{sql.user}"}

    def test_query_renames_table_from_qry_w_comments(self):
        query_string = f"""
        -- EXEC sp_rename 'RISCRASHDATA.{dsms}.old1_{sql.user}', 'new1_{sql.user}'
        /*  EXEC sp_rename 'RISCRASHDATA.{dsms}.old2_{sql.user}', 'new2_{sql.user}' */
        /*
            EXEC sp_rename 'RISCRASHDATA.{dsms}.old3_{sql.user}', 'new3_{sql.user}'
        */
            EXEC sp_rename 'RISCRASHDATA.{dsms}.test_{sql.user}', 'node_{sql.user}'
        """
        assert query.Query.query_renames_table(query_string, default_schema=dsms) == {f'{dsms}.node_{sql.user}': f'test_{sql.user}'}

    def test_query_renames_table_logging_not_temp(self):
        sql.drop_table(dsms, f'___test___test___{sql.user}___')
        assert not db.table_exists(f'___test___test___{sql.user}___', schema=dsms)
        sql.query(f"create table {dsms}.___test___test___{sql.user}___ (id int);", temp=False)
        assert sql.table_exists(f'___test___test___{sql.user}___', schema=dsms)
        assert not sql.check_table_in_log(f'___test___test___{sql.user}___', schema=dsms)

        sql.drop_table(dsms, f'___test___test___2___{sql.user}___')
        sql.query(f"EXEC sp_rename '{dsms}.___test___test___{sql.user}___', '___test___test___2___{sql.user}___'")
        assert sql.table_exists(f'___test___test___2___{sql.user}___', schema=dsms)
        assert not sql.check_table_in_log(f'___test___test___2___{sql.user}___', schema=dsms)
        sql.drop_table(dsms, f'___test___test___2___{sql.user}___')

    def test_query_renames_table_logging_temp(self):
        sql.drop_table(dsms, f'___test___test___{sql.user}___')
        assert not db.table_exists(f'___test___test___{sql.user}___', schema=dsms)
        sql.query(f"create table {dsms}.___test___test___{sql.user}___ (id int);", temp=True)
        assert sql.table_exists(f'___test___test___{sql.user}___', schema=dsms)
        assert sql.check_table_in_log(f'___test___test___{sql.user}___', schema=dsms)

        sql.drop_table(dsms, f'___test___test___2___{sql.user}___')
        sql.query(f"EXEC sp_rename '{dsms}.___test___test___{sql.user}___', '___test___test___2___{sql.user}___'")
        assert sql.table_exists(f'___test___test___2___{sql.user}___', schema=dsms)
        assert sql.check_table_in_log(f'___test___test___2___{sql.user}___', schema=dsms)
        sql.drop_table(dsms, f'___test___test___2___{sql.user}___')


class TestQueryCreatesTablesPgSql():
    def test_query_renames_table_from_qry(self):
        query_string = f"""
            ALTER TABLE {dspg}.test_{db.user}
            RENAME TO node_{db.user}
        """
        assert query.Query.query_renames_table(query_string, 'public') == {f'{dspg}.node_{db.user}': f'test_{db.user}'}

    def test_query_renames_table_from_qry_quotes(self):
        query_string = f"""
            ALTER TABLE "{dspg}"."test_{db.user}"
            RENAME TO "node_{db.user}"
        """
        assert query.Query.query_renames_table(query_string, 'public') == {f'"{dspg}"."node_{db.user}"': f'"test_{db.user}"'}

    def test_query_renames_table_from_qry_multiple(self):
        query_string = f"""
            ALTER TABLE "{dspg}"."test_{db.user}"
            RENAME TO "node_{db.user}";

            CREATE TABLE {dspg}.test_table_error_{db.user} as
            SELECT * FROM node_{db.user};

            ALTER TABLE {dspg}.test2_{db.user}
            RENAME TO node2_{db.user};
        """
        assert query.Query.query_renames_table(query_string, 'public') == {f'"{dspg}"."node_{db.user}"': f'"test_{db.user}"',
                                                                               f'{dspg}.node2_{db.user}': f'test2_{db.user}'}

    def test_query_renames_table_from_qry_w_comments(self):
        query_string = f"""
        -- ALTER TABLE {dspg}.old1_{db.user} rename to new1_{db.user}
        /*  ALTER TABLE old2_{db.user} rename to new2_{db.user} */
        /*
            ALTER TABLE {dspg}.old3_{db.user} rename to new3_{db.user}
        */
        ALTER TABLE {dspg}.test_{db.user}
        RENAME TO node_{db.user}
        """
        assert query.Query.query_renames_table(query_string, 'public') == {f'{dspg}.node_{db.user}': f'test_{db.user}'}


    def test_query_renames_table_logging_not_temp(self):
        db.drop_table(dspg, f'___test___test___{db.user}')
        assert not db.table_exists(f'___test___test___{db.user}', schema=dspg)
        db.query(f"create table {dspg}.___test___test___{db.user} (id int);", temp=False)
        assert db.table_exists(f'___test___test___{db.user}', schema=dspg)
        assert not db.check_table_in_log(f'___test___test___{db.user}', schema=dspg)

        db.drop_table(dspg, f'___test___test___2___{db.user}')
        db.query(f"alter table {dspg}.___test___test___{db.user} rename to ___test___test___2___{db.user}")
        assert db.table_exists(f'___test___test___2___{db.user}', schema=dspg)
        assert not db.check_table_in_log(f'___test___test___2___{db.user}', schema=dspg)
        db.drop_table(dspg, f'___test___test___2___{db.user}')

    def test_query_renames_table_logging_temp(self):
        db.drop_table(dspg, f'___test___test___{db.user}')
        assert not db.table_exists(f'___test___test___{db.user}', schema=dspg)
        db.query(f"create table {dspg}.___test___test___{db.user} (id int);", temp=True)
        assert db.table_exists(f'___test___test___{db.user}', schema=dspg)
        assert db.check_table_in_log(f'___test___test___{db.user}', schema=dspg)

        db.drop_table(dspg, f'___test___test___2___{db.user}')
        db.query(f"alter table {dspg}.___test___test___{db.user} rename to ___test___test___2___{db.user} ")
        assert db.table_exists(f'___test___test___2___{db.user}', schema=dspg)
        assert db.check_table_in_log(f'___test___test___2___{db.user}', schema=dspg)
        db.drop_table(dspg, f'___test___test___2___{db.user}')

