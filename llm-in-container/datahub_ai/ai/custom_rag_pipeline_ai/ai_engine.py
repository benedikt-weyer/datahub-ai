import dotenv
import os

from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import PromptTemplate

from sqlalchemy import create_engine
from sqlalchemy.sql import text


from datahub_ai.logic import data_description_logic
from datahub_ai.ai.custom_rag_pipeline_ai import table_selector, sql_query_generator, response_synthesizer



def submit_query(query_string, is_verbose=False, without_docker=False, override_ollama_api_url=None, chat_history=None):

    print(f'Question: {query_string}')

    # Load the .env file
    dotenv.load_dotenv()

    # set ollama api url
    ollama_api_url = os.getenv('OLLAMA_API_URL')
    if override_ollama_api_url is not None:
        ollama_api_url = override_ollama_api_url

    print(ollama_api_url)

    # set the models to use
    llm_gemma2 = Ollama(base_url=ollama_api_url, model='gemma2:9b', request_timeout=60.0)
    llm_deapsek_r1 = Ollama(base_url=ollama_api_url, model='deepseek-r1:8b', request_timeout=60.0)
    llm_sqlcoder = Ollama(base_url=ollama_api_url, model='sqlcoder:7b', request_timeout=60.0)
    llm_dolphin_llama3 = Ollama(base_url=ollama_api_url, model='dolphin-llama3:8b', request_timeout=60.0)
    embedding_mxbai= OllamaEmbedding(base_url=ollama_api_url, model_name='mxbai-embed-large:latest', request_timeout=60.0)

    # init models
    embedding_standard_embedding = embedding_mxbai
    llm_table_selector = llm_gemma2
    llm_chat_assistent = llm_gemma2
    llm_sql_query_generation = llm_gemma2
    llm_response_synthesizer = llm_deapsek_r1
    

    # init chat engine
    chat_assistant_engine = SimpleChatEngine.from_defaults(llm=llm_chat_assistent, embedding=embedding_standard_embedding, chat_history=chat_history)
    

    # get table infos
    table_infos = data_description_logic.get_active_tables(without_docker)
    table_infos_formated = [{'table_name': table.get('table_name'), 'table_description': table.get('table_description')} for table in table_infos]

    # create database engine
    database_url = f'postgresql://didex:didex@{"localhost" if without_docker else "postgis"}:5432/didex'
    engine = create_engine(database_url)

    # get the column info for the relevant tables
    # with engine.connect() as connection:
    #     for i, table_info in enumerate(table_infos_formated):
    #         table_name = table_info['table_name']

    #         query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = 'public'"


    #         result = connection.execute(text(query))
    #         columns = [{'column_name': row[0], 'data_type': row[1]} for row in result]
    #         # update relevant_table_infos directly
    #         table_infos_formated[i]['columns'] = columns


    # get relevant tables
    table_selector_response = table_selector.select_important_tables(query_string, table_infos_formated, llm_table_selector)
    relevant_table_names = table_selector_response['relavant_tables']
    is_sql_query_necessary = table_selector_response['is_sql_query_necessary']

    if is_sql_query_necessary:

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

        # generate sql query
        sql_query_generation_response = sql_query_generator.generate_sql_query(query_string, relevant_table_infos, llm_sql_query_generation)
        sql_query = sql_query_generation_response['sql_query']

        print(relevant_table_infos)

        print(sql_query)

        if sql_query is None:
            response = "Sorry, I could not generate a valid SQL query for the given question."
            return {
                "response": response,
                "chat_history": chat_assistant_engine.chat_history,
            }

        # execute sql query
        sql_query_results = None
        with engine.connect() as connection:
            connection.execute(text("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY"))
            result = connection.execute(text(sql_query))
            sql_query_results = [dict(row) for row in result.mappings()]
            #print(response)


        # synthesise response
        response = response_synthesizer.synthesize_response(query_string, sql_query_results, sql_query, llm_response_synthesizer)['synthesized_response']


    else:
        response = chat_assistant_engine.chat(query_string)
        


    # RESPONSE_TMPL = (
    #     "Repeat back the question in a more structured way, to the user and state the tables that are relevant to the question \n"
    #     "Question: {query_string}\n"
    #     "Relevant Tables: {relevant_tables}\n"
    # )
    # RESPONSE_PROMPT = PromptTemplate(RESPONSE_TMPL)
    # response_prompt_string = RESPONSE_PROMPT.format(query_string=query_string, relevant_tables=relevant_tables)


    # response = chat_engine.chat(response_prompt_string)
    


    return {
        "response": response,
        "chat_history": chat_assistant_engine.chat_history,
    }