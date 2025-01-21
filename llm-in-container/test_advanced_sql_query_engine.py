import unittest
from uuid import uuid4

from llama_cloud import ChatMessage, MessageRole
from llama_index.core.llms import ChatResponse
from datahub_ai.ai import advanced_sql_query_engine

class TestAddOneToNr(unittest.TestCase):

    #def test_parse_response_to_sql_no_sql(self):
    #    message = ChatMessage(
    #        role=MessageRole.CHATBOT,
    #        content="No SQL here",
    #        id=str(uuid4()),  # Generiert eine eindeutige ID
    #        index=0  # Setzen Sie den Index entsprechend
    #    )
    #    chat_response = ChatResponse(message={"message": message})
    #    res = advanced_sql_query_engine.parse_response_to_sql(chat_response);
    #    self.assertEqual("WITH non_existent_table AS (SELECT 'no sql query provided' as error) SELECT * FROM non_existent_table;", res)

    def test_parse_respond_to_sql_sql(self):
        message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content="SQLQuery: Hello World",
            id=str(uuid4()),  # Generiert eine eindeutige ID
            index=0  # Setzen Sie den Index entsprechend
        )
        chat_response = ChatResponse(message={"message": message})
        print(type(chat_response))
        print(chat_response.__dict__)
        print(type(chat_response.message))
        print(chat_response.message.__dict__)

        #res = advanced_sql_query_engine.parse_response_to_sql(chat_response);
        self.assertEqual("SQLQuery:HelloWorld", "res")