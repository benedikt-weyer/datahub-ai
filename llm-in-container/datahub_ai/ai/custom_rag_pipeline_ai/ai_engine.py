import dotenv
import os

from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.prompts.prompt_type import PromptType
from llama_index.core import (
    SQLDatabase,
    VectorStoreIndex,
    PromptTemplate,
    set_global_handler
)

from datahub_ai.logic import data_description_logic
from datahub_ai.ai.custom_rag_pipeline_ai import table_selector


def submit_query(query_string, is_verbose=False, without_docker=False, override_ollama_api_url=None, chat_history=None):

    # Load the .env file
    dotenv.load_dotenv()

    # set ollama api url
    ollama_api_url = os.getenv('OLLAMA_API_URL')
    if override_ollama_api_url is not None:
        ollama_api_url = override_ollama_api_url

    print(ollama_api_url)

    # set the models to use
    llm_name_table_selector = "gemma2:9b"
    embedding_name_standard_embedding = "mxbai-embed-large:latest"

    # init models
    llm_table_selector = Ollama(base_url=ollama_api_url, model=llm_name_table_selector, request_timeout=30.0)
    embedding_standard_embedding = OllamaEmbedding(model_name=embedding_name_standard_embedding, base_url=ollama_api_url)

    # init chat engine
    chat_engine = SimpleChatEngine.from_defaults(llm=llm_table_selector, embedding=embedding_standard_embedding, chat_history=chat_history)
    

    # get table infos
    table_infos = data_description_logic.get_active_tables(without_docker)

    # get relevant tables
    relevant_tables = table_selector.select_important_tables(query_string, table_infos, llm_table_selector)


    RESPONSE_TMPL = (
        "Repeat back the question in a more structured way, to the user and state the tables that are relevant to the question \n"
        "Question: {query_string}\n"
        "Relevant Tables: {relevant_tables}\n"
    )
    RESPONSE_PROMPT = PromptTemplate(RESPONSE_TMPL)
    response_prompt_string = RESPONSE_PROMPT.format(query_string=query_string, relevant_tables=relevant_tables)


    response = chat_engine.chat(response_prompt_string)
    


    return {
        "response": response,
        "chat_history": chat_engine.chat_history,
    }