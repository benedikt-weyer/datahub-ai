import dotenv
import os

from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import PromptTemplate


from datahub_ai.logic import data_description_logic
from datahub_ai.ai.custom_rag_pipeline_ai import table_selector
from datahub_ai.ai.custom_rag_pipeline_ai import sql_query_generator



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
    llm_gemma2 = Ollama(base_url=ollama_api_url, model='gemma2:9b', request_timeout=30.0)
    embedding_mxbai= OllamaEmbedding(base_url=ollama_api_url, model_name='mxbai-embed-large:latest', request_timeout=30.0)

    # init models
    embedding_standard_embedding = embedding_mxbai
    llm_table_selector = llm_gemma2
    llm_chat_assistent = llm_gemma2
    llm_sql_query_generation = llm_gemma2
    

    # init chat engine
    chat_assistant_engine = SimpleChatEngine.from_defaults(llm=llm_chat_assistent, embedding=embedding_standard_embedding, chat_history=chat_history)
    

    # get table infos
    table_infos = data_description_logic.get_active_tables(without_docker)

    # get relevant tables
    table_selector_response = table_selector.select_important_tables(query_string, table_infos, llm_table_selector)
    relevant_table_names = table_selector_response['relavant_tables']
    is_sql_query_necessary = table_selector_response['is_sql_query_necessary']

    if is_sql_query_necessary:
        # get relevant table infos
        relevant_table_infos = [table_info for table_info in table_infos if table_info['table_name'] in relevant_table_names]

        # generate sql query
        sql_query_generation_response = sql_query_generator.generate_sql_query(query_string, relevant_table_infos, llm_sql_query_generation)
        sql_query = sql_query_generation_response['sql_query']


        response = sql_query
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