import unittest
from uuid import uuid4

from llama_cloud import ChatMessage, MessageRole
from llama_index.core.llms import ChatResponse
from datahub_ai.ai import advanced_sql_query_engine

class TestAdvancedSQLQueryEngine(unittest.TestCase):

    def test_parse_respond_to_sql_basic(self):
        response_str = "SQLQuery: WITH non_existent_table AS (SELECT 'no sql query provided' as error) SELECT * FROM non_existent_table;"

        chat_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response_str,
            id=str(uuid4()),  # Generiert eine eindeutige ID
            index=0  # Setzen Sie den Index entsprechend
        )
        chat_response = ChatResponse(message={"message": chat_message})


        sql = advanced_sql_query_engine.parse_response_to_sql(chat_response);


        self.assertEqual(sql, "WITH non_existent_table AS (SELECT 'no sql query provided' as error) SELECT * FROM non_existent_table;")

if __name__ == "__main__":
    unittest.main()