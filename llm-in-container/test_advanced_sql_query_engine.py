import unittest

from datahub_ai.ai import advanced_sql_query_engine

class TestAddOneToNr(unittest.TestCase):
    def test_add_once(self):
        res = advanced_sql_query_engine.add_one_to_nr(1)
        self.assertEqual(2,2)