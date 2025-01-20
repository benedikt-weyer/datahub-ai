from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

def generate_sql_query(question_string, relavent_table_info, sql_query_generation_llm: Ollama):

    TEXT_TO_SQL_TMPL = (
        "Given an input question, first create a syntactically correct Postgres SQL statement "
        #"query to run, then look at the results of the query and return the answer. "
        #"You can order the results by a relevant column to return the most "
        #"interesting examples in the database.\n\n"
        "Never query for all the columns from a specific table, only ask for a few relevant columns given the question.\n\n"

        "Pay attention to use only the column names that you can see in the schema description. \n"
        
        "Be careful to not query for columns that do not exist. \n"

        "Pay attention to which column is in which table. \n"
        # "Also, qualify column names with the table name when needed. "
        # "'id' is not short for 'index' "
        # "When asked for a shape/shapes, make the sql query return the name of the shape/shapes "

        #"When you want to filter for Countries or Regions or Districts, use shapes_shape and shapes_type and join them on shape_id=id. "
        #"Countries and Regions and Districts are writen in upercase when used in the query. "
        #"Do not use name = 'District' in this table or similar!! "
        "All the data is refering to Ghana, so do not use 'Ghana' in the query. "
        #"Do NOT use aliases (like AS)."

        "Only use tables listed below.\n"
        "Here is the data you need: \n"
        "Question: {question_string}\n"
        "Table Info: {table_info}\n"
        "\n\n"

        "Format your response as stated below, each taking one line: \n"
        "SQL_Query: SQL Query to run\n"
    )
    
    TEXT_TO_SQL_PROMPT = PromptTemplate(TEXT_TO_SQL_TMPL)
    select_table_prompt_string = TEXT_TO_SQL_PROMPT.format(question_string=question_string, table_info=relavent_table_info)

    print(select_table_prompt_string)

    output = sql_query_generation_llm.complete(select_table_prompt_string)

    print(output)

    # extract values from response
    sql_query = extract_value_from_response_string(output.text, 'SQL_Query')



    return {
        'sql_query': sql_query,
    }