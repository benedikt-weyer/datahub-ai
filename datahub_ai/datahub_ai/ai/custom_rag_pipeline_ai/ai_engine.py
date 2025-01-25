import dotenv
import os

from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.base.llms.types import ChatMessage

from sqlalchemy import create_engine
from sqlalchemy.sql import text


from datahub_ai.logic import data_description_logic, datahub_metadata_logic
from datahub_ai.ai.custom_rag_pipeline_ai import table_selector, sql_query_generator, response_synthesizer, query_preparer



def submit_query(query_string, is_verbose=False, without_docker=False, override_ollama_api_url=None, chat_store=None, chat_memory=None):

    verbose_output_submit_query = f'## Verbose output ##\n'

    print(f'Question: {query_string}')

    # Load the .env file
    dotenv.load_dotenv()

    # set ollama api url
    ollama_api_url = os.getenv('OLLAMA_API_URL')
    if override_ollama_api_url is not None:
        ollama_api_url = override_ollama_api_url

    verbose_output_submit_query += f"<b>OLLAMA API URL</b>: {ollama_api_url}\n\n"

    print(ollama_api_url)

    # set the models to use
    llm_gemma2 = Ollama(base_url=ollama_api_url, model='gemma2:9b', request_timeout=60.0)
    llm_deapsek_r1 = Ollama(base_url=ollama_api_url, model='deepseek-r1:8b', request_timeout=60.0)
    llm_sqlcoder = Ollama(base_url=ollama_api_url, model='sqlcoder:7b', request_timeout=60.0)
    llm_dolphin_llama3 = Ollama(base_url=ollama_api_url, model='dolphin-llama3:8b', request_timeout=60.0)
    embedding_mxbai= OllamaEmbedding(base_url=ollama_api_url, model_name='mxbai-embed-large:latest', request_timeout=60.0)

    # init models
    embedding_standard_embedding = embedding_mxbai
    llm_query_preparer = llm_deapsek_r1
    llm_table_selector = llm_deapsek_r1
    llm_chat_assistent = llm_gemma2
    llm_sql_query_generation = llm_gemma2
    llm_response_synthesizer = llm_deapsek_r1

    verbose_output_submit_query += fr"<b>Model for Embedding:</b> {embedding_standard_embedding.model_name}<br>"
    verbose_output_submit_query += fr"<b>Model for Query Preperation:</b> {llm_query_preparer.model}<br>"
    verbose_output_submit_query += fr"<b>Model for Table Selector:</b> {llm_table_selector.model}<br>"
    verbose_output_submit_query += fr"<b>Model for SQL Generation:</b> {llm_sql_query_generation.model}<br>"
    verbose_output_submit_query += fr"<b>Model for Response Synthesis:</b> {llm_response_synthesizer.model}<br>"
    verbose_output_submit_query += f"<b>Model for Chatting:</b> {llm_chat_assistent.model}\n\n"
    

    # init chat engine
    if chat_store is None:
        chat_store = SimpleChatStore()
    
    chat_memory = ChatMemoryBuffer.from_defaults(
        chat_store=chat_store,
        chat_store_key="user1",
    )

    chat_assistant_engine = SimpleChatEngine.from_defaults(llm=llm_chat_assistent, embedding=embedding_standard_embedding, memory=chat_memory)


    # prepare query
    query_preparer_response = query_preparer.prepare_query(query_string, chat_memory, llm_query_preparer)
    is_sql_query_necessary_in_general = query_preparer_response['is_sql_query_necessary']
    refined_question = query_preparer_response['refined_question']
    language = query_preparer_response['language']

    if not is_sql_query_necessary_in_general:
        response = chat_assistant_engine.chat(query_string).response

        out = {
            "response": response,
            "chat_store": chat_store,
        }
        if is_verbose:
            out["verbose_output"] = verbose_output_submit_query
        return out
    

    # get table infos
    table_infos = data_description_logic.get_active_tables(without_docker)
    table_infos_formated = [{'table_name': table.get('table_name'), 'table_description': table.get('table_description')} for table in table_infos]

   

    # create database engine
    database_url = f'postgresql://didex:didex@{"localhost" if without_docker else "postgis"}:5432/didex'
    engine = create_engine(database_url)


    # get relevant tables
    table_selector_response = table_selector.select_important_tables(refined_question, table_infos_formated, llm_table_selector)
    relevant_table_names = table_selector_response['relavant_tables']
    is_sql_query_necessary = table_selector_response['is_sql_query_necessary']
    reason_for_selecting_those_tables = table_selector_response['reason_for_selecting_those_tables']

    verbose_output_submit_query += f"<b>Relevant Table Names:</b> {relevant_table_names}\n"
    verbose_output_submit_query += f"<b>Is SQL Query Necessary:</b> {is_sql_query_necessary}\n"
    verbose_output_submit_query += f"<b>Reason for Selecting Tables:</b> {reason_for_selecting_those_tables}\n\n"


    if is_sql_query_necessary:

        # add query to chat store
        chat_store.add_message("user1", ChatMessage(role="user", content=query_string))

        # get relevant table infos
        relevant_table_infos = [table_info for table_info in table_infos_formated if table_info['table_name'] in relevant_table_names]

        # get the column info for the relevant tables
        with engine.connect() as connection:
            for i, table_info in enumerate(relevant_table_infos):
                table_name = table_info['table_name']

                query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = 'public'"


                result = connection.execute(text(query))
                columns = [{'column_name': row[0], 'data_type': row[1]} for row in result]
                # update relevant_table_infos directly
                relevant_table_infos[i]['columns'] = columns

        # get table metadata
        table_metadata = datahub_metadata_logic.get_datahub_tables_metadata(without_docker)
        #print(table_metadata)
        # add table metadata to table infos
        for table_info in relevant_table_infos:
            table_name = table_info['table_name']
            if table_metadata.get(table_name) is not None:
                table_info['metadata'] = table_metadata[table_name]

        # generate sql query
        sql_query_generation_response = sql_query_generator.generate_sql_query(refined_question, relevant_table_infos, reason_for_selecting_those_tables, llm_sql_query_generation)
        sql_queries = sql_query_generation_response['sql_queries']

        print(relevant_table_infos)

        print(sql_queries)

        verbose_output_submit_query += "### Generated SQL Queries:\n"
        for i, sql_query in enumerate(sql_queries, start=1):
            verbose_output_submit_query += f"**{i}.** `{sql_query}`\n\n"

        # execute sql queries
        sql_query_results = []
        for sql_query in sql_queries:
            try:
                with engine.connect() as connection:
                    connection.execute(text("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY"))
                    result = connection.execute(text(sql_query))
                    query_results = [{column: value for column, value in row.items()} for row in result.mappings()]
                    sql_query_results.append(query_results)
            except Exception as e:
                print(f"An error occurred while executing the SQL query: {sql_query}. Error: {e}")
                sql_query_results.append(f"Error executing query")

        print(sql_query_results)

        verbose_output_submit_query += f"<b>SQL Query Results:</b> {sql_query_results}\n\n"

        # synthesise response
        response = response_synthesizer.synthesize_response(refined_question, sql_query_results, sql_queries, relevant_table_infos, llm_response_synthesizer)['synthesized_response']

        # add response to chat store
        chat_store.add_message("user1", ChatMessage(role="assistant", content=response))


    else:
        response = chat_assistant_engine.chat(query_string).response
            


    out = {
        "response": response,
        "chat_store": chat_store,
    }
    
    if is_verbose:
        out["verbose_output"] = verbose_output_submit_query
    
    return out