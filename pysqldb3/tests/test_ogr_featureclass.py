import os
from configparser import ConfigParser
from . import helpers
from ogr_cmds import *

config = ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "\\db_config.cfg")

class TestOGRFeatureclass():

    @classmethod
    def setup(cls):
        # Set up featureclass if it doesn't exist
        if not os.path.exists('tests/test_data/lion/lion.gdb'):
            helpers.set_up_feature_class()

    def test_ogr_pg_to_featureclass(self):
        pg = helpers.get_pg_dbc_instance()
        
        # set up test data

    def test_ogr_ms_to_featureclass(self):
        ms = helpers.get_ms_dbc_instance()