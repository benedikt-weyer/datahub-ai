import dotenv
import os

from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.embeddings.ollama import OllamaEmbedding


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

    chat_engine = SimpleChatEngine.from_defaults(llm=llm_table_selector, embedding=embedding_standard_embedding, chat_history=chat_history)
    #print(chat_engine.chat("Hi, my name is Mirna"))
    #assistant: 
    #Hi Mirna! It's nice to meet you. What can I assist you with today?
    #print(chat_engine.chat("What is my name?"))

    response = chat_engine.chat(query_string)


    return {
        "response": response,
        "chat_history": chat_engine.chat_history,
    }



output = submit_query("What is the capital of France?", is_verbose=True, without_docker=True)
print(output['response'])

output2 = submit_query("Hand how big is it?", is_verbose=True, without_docker=True, chat_history=output['chat_history'])
print(output2['response'])