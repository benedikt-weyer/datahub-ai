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


from datahub_ai.logic import data_description_logic, datahub_metadata_logic, ai_query_execution
from datahub_ai.ai.custom_rag_pipeline_ai import table_selector, sql_query_generator, response_synthesizer, query_preparer, link_hydration


# Load the .env file on module import
dotenv.load_dotenv()


def submit_query(query_string, is_verbose=False, without_docker=False, override_ollama_api_url=None, chat_store=None):

    # create verbose output string for the verbose chat mode
    verbose_output_string = f'## Verbose output ##\n'

    # set ollama api url
    ollama_api_url = os.getenv('OLLAMA_API_URL')
    if override_ollama_api_url is not None:
        ollama_api_url = override_ollama_api_url

    # add ollama api url to the verbose output
    verbose_output_string += f"<b>OLLAMA API URL</b>: {ollama_api_url}\n\n"

    # initialize the models to use
    llm_gemma2 = Ollama(base_url=ollama_api_url, model='gemma2:9b', request_timeout=60.0, temperature=0.1)
    llm_deapsek_r1 = Ollama(base_url=ollama_api_url, model='deepseek-r1:8b', request_timeout=60.0, temperature=0.1)
    llm_sqlcoder = Ollama(base_url=ollama_api_url, model='sqlcoder:7b', request_timeout=60.0)
    llm_dolphin_llama3 = Ollama(base_url=ollama_api_url, model='dolphin-llama3:8b', request_timeout=60.0)
    embedding_mxbai = OllamaEmbedding(base_url=ollama_api_url, model_name='mxbai-embed-large:latest', request_timeout=60.0)

    # set the models to use
    embedding_standard_embedding = embedding_mxbai
    llm_query_preparer = llm_deapsek_r1
    llm_table_selector = llm_deapsek_r1
    llm_chat_assistent = llm_gemma2
    llm_sql_query_generation = llm_gemma2
    llm_response_synthesizer = llm_deapsek_r1

    # add the used ai models to the verbose output
    verbose_output_string += fr"<b>Model for Embedding:</b> {embedding_standard_embedding.model_name}<br>"
    verbose_output_string += fr"<b>Model for Query Preperation:</b> {llm_query_preparer.model}<br>"
    verbose_output_string += fr"<b>Model for Table Selector:</b> {llm_table_selector.model}<br>"
    verbose_output_string += fr"<b>Model for SQL Generation:</b> {llm_sql_query_generation.model}<br>"
    verbose_output_string += fr"<b>Model for Response Synthesis:</b> {llm_response_synthesizer.model}<br>"
    verbose_output_string += f"<b>Model for Chatting:</b> {llm_chat_assistent.model}\n\n"
    

    # init or set the active chat store and chat memory
    chat_store_user_key = 'user1'
    active_chat_store = chat_store

    if active_chat_store is None:
        active_chat_store = SimpleChatStore()
    
    chat_memory = ChatMemoryBuffer.from_defaults(
        chat_store=active_chat_store,
        chat_store_key=chat_store_user_key
    )


    # initialize the chat assistant engine (for answering simple questions)
    chat_assistant_engine = SimpleChatEngine.from_defaults(llm=llm_chat_assistent, embedding=embedding_standard_embedding, memory=chat_memory)


    # ----------------- Query Preparer ----------------- #
    is_sql_query_necessary_in_general = True

    # execute query preparer
    query_preparer_response = query_preparer.prepare_query(query_string, chat_memory, llm_query_preparer)

    # extract values from query preparer response
    is_sql_query_necessary_in_general = query_preparer_response['is_sql_query_necessary']
    language = query_preparer_response['language']
    prepare_query_prompt_string = query_preparer_response['prepare_query_prompt_string']
    prepare_query_llm_output = query_preparer_response['output']
    # if question is the first question asked and the language is English, the question is not refined (because the refinement process is not so refined yet)
    if chat_store is None and language == 'English':
        refined_question = query_string
    else:
        refined_question = query_preparer_response['refined_question']

    
    # add query preparer response to the verbose output
    verbose_output_string += f"<b>Prepare Query Prompt String:</b> {prepare_query_prompt_string}\n"
    verbose_output_string += f"<b>Prepare Query LLM Output:</b> {prepare_query_llm_output}\n\n"
    verbose_output_string += f"<b>Language of original Question:</b> {language}<br>"
    verbose_output_string += f"<b>Refined Question:</b> {refined_question}\n\n"

    

    # ----------------- Simple Chat Assistant + Return ----------------- #
    # if the sql query is not necessary in general, the chat assistant can answer the question
    if not is_sql_query_necessary_in_general:
        # get the response from the chat assistant
        response = chat_assistant_engine.chat(query_string).response

        out = {
            "response": response,
            "chat_store": active_chat_store,
        }
        if is_verbose:
            out["verbose_output"] = verbose_output_string

        return out
    
    # ----------------- Table Selector Agent ----------------- #

    # get table infos from the active tables
    table_infos = data_description_logic.get_active_tables(without_docker)
    # filter out the _id information
    table_infos_formated = [{'table_name': table.get('table_name'), 'table_description': table.get('table_description')} for table in table_infos]
    # get the table names
    table_names = [table_info['table_name'] for table_info in table_infos_formated]

    # execute table selector
    table_selector_response = table_selector.select_important_tables(refined_question, table_infos_formated, llm_table_selector)

    # extract values from table selector response
    relevant_table_names = table_selector_response['relavant_tables']
    is_sql_query_necessary = table_selector_response['is_sql_query_necessary']
    reason_for_selecting_those_tables = table_selector_response['reason_for_selecting_those_tables']
    select_table_prompt_string = table_selector_response['select_table_prompt_string']
    select_table_llm_output = table_selector_response['output']

    # add table selector response to the verbose output
    verbose_output_string += f"<b>Select Table Prompt String:</b> {select_table_prompt_string}\n"
    verbose_output_string += f"<b>Select Table LLM Output:</b> {select_table_llm_output}\n"
    verbose_output_string += f"<b>Relevant Table Names:</b> {relevant_table_names}\n"
    verbose_output_string += f"<b>Is SQL Query Necessary:</b> {is_sql_query_necessary}\n"
    verbose_output_string += f"<b>Reason for Selecting Tables:</b> {reason_for_selecting_those_tables}\n\n"


    # ----------------- Simple Chat Assistant + Return ----------------- #
    # if the sql query is not necessary, the chat assistant can answer the question
    if not is_sql_query_necessary:
        # get the response from the chat assistant
        response = chat_assistant_engine.chat(query_string).response

        out = {
            "response": response,
            "chat_store": active_chat_store,
        }
        if is_verbose:
            out["verbose_output"] = verbose_output_string

        return out
    

    # ----------------- SQL Query Generator ----------------- #

    # filter out the relevant table infos
    relevant_table_infos = [table_info for table_info in table_infos_formated if table_info['table_name'] in relevant_table_names]

    relevant_table_names_proved = [table_info['table_name'] for table_info in relevant_table_infos]

    # get the column info for the relevant tables
    column_info = datahub_metadata_logic.get_column_info_from_tables(relevant_table_names_proved, without_docker=without_docker)

    # add the column info to the relevant table infos
    for table_info in relevant_table_infos:
        table_name = table_info['table_name']
        table_info['columns'] = column_info[table_name]
    

    # get table metadata from datahub
    table_metadata = datahub_metadata_logic.get_datahub_tables_metadata(without_docker)

    # add table metadata to table infos
    for table_info in relevant_table_infos:
        table_name = table_info['table_name']
        if table_metadata.get(table_name) is not None:
            table_info['metadata'] = table_metadata[table_name]


    # generate sql query
    sql_query_generation_response = sql_query_generator.generate_sql_query(refined_question, relevant_table_infos, reason_for_selecting_those_tables, llm_sql_query_generation)
    # extract values from sql query generation response
    sql_queries = sql_query_generation_response['sql_queries']

    # add sql query generation response to the verbose output
    verbose_output_string += "\n#### Generated SQL Queries:\n"
    for i, sql_query in enumerate(sql_queries, start=1):
        verbose_output_string += f"**{i}.** `{sql_query}`\n\n"


    # ----------------- SQL Query Execution ----------------- #
    # execute sql queries
    sql_query_results = []
    for sql_query in sql_queries:
        try:
            # execute the sql query
            query_result = ai_query_execution.execute_generated_query(sql_query, without_docker=without_docker)
            # append the query result to the sql_query_results
            sql_query_results.append(query_result)

        except Exception:
            # append an error message to the sql_query_results
            sql_query_results.append(f"Error executing query")

    # add sql query results to the verbose output
    verbose_output_string += f"<b>SQL Query Results:</b> {sql_query_results}\n\n"

    # ----------------- Response Synthesizer ----------------- #
    # synthesise response
    response_synthesizer_response = response_synthesizer.synthesize_response(refined_question, sql_query_results, sql_queries, relevant_table_infos, llm_response_synthesizer)
    # extract values from response synthesizer
    response = response_synthesizer_response['synthesized_response']



    # add user query to chat store
    active_chat_store.add_message(chat_store_user_key, ChatMessage(role="user", content=query_string))

    # add response to chat store
    active_chat_store.add_message(chat_store_user_key, ChatMessage(role="assistant", content=response))
        


    # link hydration for the response with the datalayer url
    response = link_hydration.hydrate_response_with_datalayer_url(response, table_names)

    
    # return the response and the chat store (and the verbose output if is_verbose is True)
    out = {
        "response": response,
        "chat_store": active_chat_store,
    }
    
    if is_verbose:
        out["verbose_output"] = verbose_output_string
    
    return out