from sqlalchemy import create_engine , inspect
from llama_index.llms.ollama import Ollama
from llama_index.core import SQLDatabase, Response
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.embeddings.ollama import OllamaEmbedding
import networkx as nx


class LLMQueryEngine:
   #_instance: Optional["LLMQueryEngine"] = None  # Singleton instance holder

    #def __new__(cls, *args, **kwargs):
     #   if cls._instance is None:
      #      cls._instance = super().__new__(cls)
       # return cls._instance

    def __init__(self, DB_URL: str = 'postgresql://didex:didex@postgis:5432/didex',
                LLM_BASE_URL: str = 'http://benedikt-home-server.duckdns.org:11434',
                MODEL="dolphin-llama3:latest",
                EMBEDDING_MODEL="mx-bai-embed-large"):
        if not hasattr(self, "initialized"):  # Prevent reinitialization
            self.initialized = True
            self.database_url = DB_URL
            self.engine = create_engine(self.database_url)
            self.inspector = inspect(self.engine)
            self.table_names = self.inspector.get_table_names()

            self.LLM = Ollama(base_url=LLM_BASE_URL,
                              model=MODEL,
                              request_timeout=60.0)
            self.embedding = OllamaEmbedding(model_name=EMBEDDING_MODEL,
                                             base_url=LLM_BASE_URL)
            self.sql_database = SQLDatabase(self.engine,
                                            include_tables=self.table_names)

            self.query_engine = NLSQLTableQueryEngine(sql_database=self.sql_database,
                                                      tables=self.table_names,
                                                      verbose=True,
                                                      embed_model=self.embedding,
                                                      llm=self.LLM)
            self.graph = nx.DiGraph()
    
    def submit_query(self, query_string: str) -> Response:
        response: Response = self.query_engine.query(query_string)
        self._update_graph(query_string, response.response)
        return response
    
    def _update_graph(self, query, answer):
        self.graph.add_node(query, type='query')
        self.graph.add_node(answer, type='response')
        self.graph.add_edge(query, answer)
        
    
    
#llm = LLMQueryEngine()

#response = llm.submit_query("what is the size of largest area in sqm?")

#print(response.response)