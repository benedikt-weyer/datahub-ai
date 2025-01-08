from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


from llama_index.core.llms import ChatMessage
import dotenv
import os

dotenv.load_dotenv()
ollama_api_url = os.getenv('OLLAMA_API_URL')
print(ollama_api_url)


llm = Ollama(base_url=ollama_api_url, model="dolphin-llama3:latest", request_timeout=30.0)
#llm_synth = OpenAI(model="gpt-3.5-turbo")

llm_sql = Ollama(base_url=ollama_api_url, model="gemma2:9b", request_timeout=30.0)
#llm_sql = Ollama(base_url=ollama_api_url, model="mistral:latest", request_timeout=60.0)
#llm_sql = OpenAI(model="gpt-4o-mini")


#llm_summary = Ollama(base_url=ollama_api_url, model="dolphin-llama3:latest", request_timeout=30.0)

#init embedding
ollama_embedding = OllamaEmbedding(
    model_name="mxbai-embed-large",
    #model_name="nomic-embed-text",
    base_url=ollama_api_url,
    #ollama_additional_kwargs={"mirostat": 0},
)

#resp = llm.complete("Who is Paul Graham?")
resp = llm.chat([
    ChatMessage(role="user", content="Who is Paul Graham?"),
    ChatMessage(role="user", content="What did I ask before?")
])
print(resp)

#resp2 = llm.complete("What did I ask before?")
resp2 = llm.chat([
    ChatMessage(role="user", content="What did I ask before?")
])
print(resp2)

# messages = [
#     ChatMessage(
#         role="system", content="You are a pirate with a colorful personality"
#     ),
#     ChatMessage(role="user", content="What is your name"),
# ]
