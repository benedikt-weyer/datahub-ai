from logic import data_description_logic

from sqlalchemy import create_engine, MetaData, inspect

from llama_index.llms.ollama import Ollama
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding

from llama_index.core.retrievers import SQLRetriever

from llama_index.core.retrievers import SQLRetriever
from typing import List
from llama_index.core.query_pipeline import FnComponent

from llama_index.core.objects import (
    SQLTableSchema
)

from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_TO_SQL_PROMPT
from llama_index.core import PromptTemplate
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.llms import ChatResponse

from IPython.display import display, HTML

from pyvis.network import Network

from llama_index.llms.openai import OpenAI

from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType

import llama_index.core

 # setup Arize Phoenix for logging/observability
import phoenix as px

import dotenv
import os

def submit_query(query_str, is_verbose, without_docker=False, override_ollama_api_url=None):
    # Load the .env file
    dotenv.load_dotenv()

    print(os.getenv('OLLAMA_API_URL'))

    # set ollama api url
    ollama_api_url = os.getenv('OLLAMA_API_URL')
    if override_ollama_api_url is not None:
        ollama_api_url = override_ollama_api_url
   

    px.launch_app()
    llama_index.core.set_global_handler("arize_phoenix")

    
    llm_synth = Ollama(base_url=ollama_api_url, model="dolphin-llama3:latest", request_timeout=30.0)
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

    #create database engine
    database_url = f'postgresql://didex:didex@{"localhost" if without_docker else "postgis"}:5432/didex'
    engine = create_engine(database_url)


    #create databse
    sql_database = SQLDatabase(engine)

    #create sql retriever
    sql_retriever = SQLRetriever(sql_database)


    # get table infos / table descriptions + active tables
    table_infos = data_description_logic.get_active_tables()
    print(table_infos, flush=True)



    def get_table_context_str(table_schema_objs: List[SQLTableSchema]):
        """Get table context string."""
        context_strs = []
        for table_schema_obj in table_schema_objs:
            table_info = sql_database.get_single_table_info(
                table_schema_obj.table_name
            )
            if table_schema_obj.context_str:
                table_opt_context = " The table description is: "
                table_opt_context += table_schema_obj.context_str
                table_info += table_opt_context

            context_strs.append(table_info)
        return "\n\n".join(context_strs)

    table_parser_component = FnComponent(fn=get_table_context_str)


    table_node_mapping = SQLTableNodeMapping(sql_database)

    table_schema_objs = [
        SQLTableSchema(table_name=table.get('table_name'), context_str=table.get('table_description'))
        for table in table_infos
    ]  # add a SQLTableSchema for each table

    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex,
        embed_model=ollama_embedding
    )
    obj_retriever = obj_index.as_retriever(similarity_top_k=3)




    def parse_response_to_sql(response: ChatResponse) -> str:
        

        sql_query = ''

        #extract message content
        message_content = response.message.content

        print('####')
        print(response)
        print('####')

        #find sql query location
        sql_query_start = message_content.find("SQLQuery:")
        #sql_query_end = message_content.find("SQLResult:")

        #extract sql query
        if sql_query_start != -1:
            sql_query = message_content[sql_query_start + len("SQLQuery:"):]
        else: 
            #error: no sql query found
            return "WITH non_existent_table AS (SELECT 'no sql query provided' as error) SELECT * FROM non_existent_table;"


        #format & error correct sql query
        sql_query = sql_query.strip()
        sql_query = sql_query.strip("```")
        sql_query = sql_query.replace("`", "")
        sql_query = sql_query.strip()

        return sql_query


    sql_parser_component = FnComponent(fn=parse_response_to_sql)

    MODIFIED_TEXT_TO_SQL_TMPL = (
        "Given an input question, first create a syntactically correct {dialect} "
        "query to run, then look at the results of the query and return the answer. "
        "You can order the results by a relevant column to return the most "
        "interesting examples in the database.\n\n"
        "Never query for all the columns from a specific table, only ask for a "
        "few relevant columns given the question.\n\n"
        "Pay attention to use only the column names that you can see in the schema "
        "description. "
        "Be careful to not query for columns that do not exist. "
        "Pay attention to which column is in which table. "
        "Also, qualify column names with the table name when needed. "

        "Provide an valid Postgres SQL statement."
        #"Do NOT use aliases (like AS)."

        "You are required to use the following format, each taking one line:\n\n"
        "Question: Question here\n"
        "SQLQuery: SQL Query to run\n\n"
        #"SQLResult: Result of the SQLQuery\n"
        #"Answer: Final answer here\n\n"
        "Only use tables listed below.\n"
        "{schema}\n\n"
        "Question: {query_str}\n"
        #"SQLQuery: "
    )

    MODIFIED_TEXT_TO_SQL_PROMPT = PromptTemplate(
        MODIFIED_TEXT_TO_SQL_TMPL,
        prompt_type=PromptType.TEXT_TO_SQL,
    )

    text2sql_prompt = MODIFIED_TEXT_TO_SQL_PROMPT.partial_format(dialect=engine.dialect.name)
    #text2sql_prompt = DEFAULT_TEXT_TO_SQL_PROMPT.partial_format(dialect=engine.dialect.name)

    response_synthesis_prompt_str = (
        "Given an input question, synthesize a response from the query results.\n"
        "Also always mention the queried tables aka the used datasources. \n"
        "Query: {query_str}\n"
        "SQL: {sql_query}\n"
        "SQL Response: {context_str}\n"
        "Response: "
    )
    response_synthesis_prompt = PromptTemplate(
        response_synthesis_prompt_str,
    )


    from llama_index.core.query_pipeline import (
        QueryPipeline as QP,
        Link,
        InputComponent,
        CustomQueryComponent,
    )

    qp = QP(
        modules={
            "input": InputComponent(),
            "table_retriever": obj_retriever,
            "table_output_parser": table_parser_component,
            "text2sql_prompt": text2sql_prompt,
            "text2sql_llm": llm_sql,
            "sql_output_parser": sql_parser_component,
            "sql_retriever": sql_retriever,
            "response_synthesis_prompt": response_synthesis_prompt,
            "response_synthesis_llm": llm_synth,
        },
        verbose=True,
    )


    qp.add_chain(["input", "table_retriever", "table_output_parser"])
    qp.add_link("input", "text2sql_prompt", dest_key="query_str")
    qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
    qp.add_chain(
        ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
    )
    qp.add_link(
        "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
    )
    qp.add_link(
        "sql_retriever", "response_synthesis_prompt", dest_key="context_str"
    )
    qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
    qp.add_link("response_synthesis_prompt", "response_synthesis_llm")




    net = Network(notebook=False, cdn_resources="in_line", directed=True)
    net.from_nx(qp.dag)


    # Save the network as "text2sql_dag.html"
    net.write_html("text2sql_dag.html")


    # Read the contents of the HTML file
    with open("text2sql_dag.html", "r") as file:
        html_content = file.read()

    # Display the HTML content
    display(HTML(html_content))


    response = qp.run(
        query=query_str
        #query="I need a quick overview of the Ada East district, Ghana. How large is this district and how many people live there?"
        #query="I need the location of all schools in Kumasi district, Ghana. Is this dataset available?"
        #query="For my research project on malaria, I need precipitation data for the period from January 2020 to December 2023. Are these data available, and in what resolution?"
        #query="What regions are found in the data?"
    )

    return str(response.message.content)