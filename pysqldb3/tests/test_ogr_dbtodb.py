import os
import pytest
from .. import ogr_cmds
from . import TestHelpers

class TestOGRDBtoDB():

    @pytest.mark.ogr
    def test_ogr_pg_to_ms(self):

        # connect to dbs
        pg = TestHelpers.get_pg_dbc_instance()
        ms = TestHelpers.get_ms_dbc_instance()
        pg.connect()
        ms.connect()
        test_tbl_name = f"test_ogr_pg_to_mssql_{pg.user}"

        # drop test table if it exists
        if pg.table_exists(test_tbl_name):
            pg.drop_table(test_tbl_name)
        if ms.table_exists(test_tbl_name):
            ms.drop_table(test_tbl_name)
        assert not (pg.table_exists(test_tbl_name) or ms.table_exists(test_tbl_name))

        # create test table in pg and assert existence
        TestHelpers.set_up_simple_test_table_pg(pg, table_name=test_tbl_name)
        assert pg.table_exists(test_tbl_name)

        # perform OGR command
        ogr_cmds.pgsql_to_mssql(pg_table=test_tbl_name, ms_table=test_tbl_name, use_ldap=False, spatial=False)

        # assert new table existence in ms
        assert ms.table_exists(test_tbl_name)

    @pytest.mark.ogr
    def test_ogr_pg_to_ms_spatial(self):
        # connect to dbs
        pg = TestHelpers.get_pg_dbc_instance()
        ms = TestHelpers.get_ms_dbc_instance()
        pg.connect()
        ms.connect()
        test_tbl_name = f"test_ogr_pg_to_mssql_spatial_{pg.user}"

        # drop test table if it exists
        if pg.table_exists(test_tbl_name):
            pg.drop_table(test_tbl_name)
        if ms.table_exists(test_tbl_name):
            ms.drop_table(test_tbl_name)
        assert not (pg.table_exists(test_tbl_name) or ms.table_exists(test_tbl_name))

        # create test table in pg and assert existence
        TestHelpers.set_up_test_table_pg(pg)
        assert pg.table_exists(test_tbl_name)

        # perform OGR command
        ogr_cmds.pgsql_to_mssql(pg_table=test_tbl_name, ms_table=test_tbl_name, use_ldap=False, spatial=True)

        # assert new table existence in ms
        assert ms.table_exists(test_tbl_name)
        

    def test_ogr_ms_to_pg(self):
        # connect to dbs
        pg = TestHelpers.get_pg_dbc_instance()
        ms = TestHelpers.get_ms_dbc_instance()
        pg.connect()
        ms.connect()
        test_tbl_name = f"test_ogr_mssql_to_pg_{ms.user}"

        # drop test table if it exists
        if pg.table_exists(test_tbl_name):
            pg.drop_table(test_tbl_name)
        if ms.table_exists(test_tbl_name):
            ms.drop_table(test_tbl_name)
        assert not (pg.table_exists(test_tbl_name) or ms.table_exists(test_tbl_name))

        # create test table in ms and assert existence
        TestHelpers.set_up_simple_test_table_sql(ms, table_name=test_tbl_name)
        assert ms.table_exists(test_tbl_name)

        # perform OGR command
        ogr_cmds.mssql_to_pgsql(ms_table=test_tbl_name, pg_table=test_tbl_name, use_ldap=False, spatial=False)

        # assert new table existance in pg
        assert pg.table_exists(test_tbl_name)
    
    def test_ogr_ms_to_pg_spatial(self):
        # connect to dbs
        ms = TestHelpers.get_ms_dbc_instance()
        pg = TestHelpers.get_pg_dbc_instance()
        ms.connect()
        pg.connect()
        test_tbl_name = f"test_ogr_mssql_to_pg_spatial_{ms.user}"

        # drop test table if it exists
        if pg.table_exists(test_tbl_name):
            pg.drop_table(test_tbl_name)
        if ms.table_exists(test_tbl_name):
            ms.drop_table(test_tbl_name)
        assert not (pg.table_exists(test_tbl_name) or ms.table_exists(test_tbl_name))

        # create test table in ms and assert existence
        TestHelpers.set_up_test_table_sql(ms, table_name=test_tbl_name)
        assert ms.table_exists(test_tbl_name)

        # perform OGR command
        ogr_cmds.mssql_to_pgsql(ms_table=test_tbl_name, pg_table=test_tbl_name, use_ldap=False, spatial=True)

        # assert new table existance in pg
        assert pg.table_exists(test_tbl_name)

    def test_ogr_pg_to_pg(self):
        # connect to dbs
        pg1 = TestHelpers.get_pg_dbc_instance()
        pg2 = TestHelpers.get_pg_dbc_instance(section_prefix='SECOND')
        pg1.connect()
        pg2.connect()
        test_tbl_name = f"test_ogr_pg_to_pg_{pg1.user}"

        # drop test tables if they exist
        if pg1.table_exists(test_tbl_name):
            pg1.drop_table(test_tbl_name)
        if pg2.table_exists(test_tbl_name):
            pg2.drop_table(test_tbl_name)
        assert not (pg1.table_exists(test_tbl_name) or pg2.table_exists(test_tbl_name))

        # perform OGR command
        ogr_cmds.pgsql_to_pgsql(source_table=test_tbl_name, dest_table=test_tbl_name, spatial=False)
        assert pg2.table_exists(test_tbl_name)

    def test_ogr_ms_to_ms(self):
        # connect to dbs
        ms1 = TestHelpers.get_ms_dbc_instance()
        ms2 = TestHelpers.get_ms_dbc_instance(section_prefix='SECOND')
        ms1.connect()
        ms2.connect()
        test_tbl_name = f"test_ogr_ms_to_ms_{ms1.user}"

        # drop test tables if they exist
        if ms1.table_exists(test_tbl_name):
            ms1.drop_table(test_tbl_name)
        if ms2.table_exists(test_tbl_name):
            ms2.drop_table(test_tbl_name)
        assert not (ms1.table_exists(test_tbl_name) or ms2.table_exists(test_tbl_name))

        # perform OGR command
        ogr_cmds.mssql_to_mssql(source_table=test_tbl_name, dest_table=test_tbl_name, spatial=False)
        assert ms2.table_exists(test_tbl_name)

    def test_ogr_ms_to_ms_spatial(self):
        # connect to dbs
        ms1 = TestHelpers.get_ms_dbc_instance()
        ms2 = TestHelpers.get_ms_dbc_instance(section_prefix='SECOND')
        ms1.connect()
        ms2.connect()
        test_tbl_name = f"test_ogr_ms_to_ms_spatial_{ms1.user}"

        # drop test tables if they exist
        if ms1.table_exists(test_tbl_name):
            ms1.drop_table(test_tbl_name)
        if ms2.table_exists(test_tbl_name):
            ms2.drop_table(test_tbl_name)
        assert not (ms1.table_exists(test_tbl_name) or ms2.table_exists(test_tbl_name))

        # perform OGR command
        ogr_cmds.mssql_to_mssql(source_table=test_tbl_name, dest_table=test_tbl_name, spatial=True)
        assert ms2.table_exists(test_tbl_name)