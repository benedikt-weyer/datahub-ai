import unittest
from uuid import uuid4

from llama_cloud import ChatMessage, MessageRole
from llama_index.core.llms import ChatResponse
from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

class TestAI(unittest.TestCase):

    def test_parse_respond_to_sql_basic(self):
        response_str = "SQLQuery: WITH non_existent_table AS (SELECT 'no sql query provided' as error) SELECT * FROM non_existent_table;"


        sql = extract_value_from_response_string(response_str, 'SQLQuery');


        self.assertEqual(sql, "WITH non_existent_table AS (SELECT 'no sql query provided' as error) SELECT * FROM non_existent_table;")

if __name__ == "__main__":
    unittest.main()