from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string
import json

def generate_sql_query(question_string, relavent_table_info, reason_for_selecting_those_tables, sql_query_generation_llm: Ollama):

    TEXT_TO_SQL_TMPL = (
        #"Given an input question, first create a syntactically correct Postgres SQL statement \n\n"
        "Given an input question, first create the needed syntactically correct Postgres SQL statements. \n"
        "One to four queries are allowed. \n\n"

        #"query to run, then look at the results of the query and return the answer. "
        #"You can order the results by a relevant column to return the most "
        #"interesting examples in the database.\n\n"
        "Never query for all the columns from a specific table; only ask for a few relevant columns given the question.\n\n"

        "Pay attention to use only the column names that you can see in the schema description. \n"
        
        "Be careful to not query for columns that do not exist. \n"

        "Pay attention to which column is in which table. \n"
        "Also, qualify column names with the table name when needed. \n"
        "'id' is not short for 'index'  \n"
        # "When asked for a shape/shapes, make the sql query return the name of the shape/shapes "

        "When asked if data is available in a given time period, then don't query for all the specific data but instead test if it exists and how many datapoints there are \n"
        "When asked for a specific urbanization rate, don't use count \n"

        #"When you want to filter for Countries or Regions or Districts, use shapes_shape and shapes_type and join them on shape_id=id. "
        #"Countries and Regions and Districts are writen in upercase when used in the query. "
        #"Do not use name = 'District' in this table or similar!! "
        "All the data is referring to Ghana, so do not use 'Ghana' in the query.  \n"
        #"Do NOT use aliases (like AS)."

        "In 'Table Info' you can find the names of the tables, the descriptions of the tables, and the corresponding columns (name and data-type). The table info is formatted in JSON. \n"

        "Only use tables listed below.\n"
        "Be careful to use the exact table names! Do not change them! .\n"
        "Do not provide the sql query like this: ```sql query```, instead use the given format. \n"

        "Here is the data you need: \n"
        "Question: {question_string}\n"
        "Table Info: {relavent_table_info}\n"
        "Reason_For_Selecting_Those_Tables: {reason_for_selecting_those_tables}\n"
        "\n\n"

        "Important!!!: Format your response exactly as stated below, taking one line: \n"
        "SQL_Query_1: sql query 1 here \n"
        "SQL_Query_2: sql query 2 here \n"
        "SQL_Query_3: sql query 3 here \n"
        "SQL_Query_4: sql query 4 here \n"
        "SQL_Queries_Count: number of needed sql queries \n\n"
    )
    
    TEXT_TO_SQL_PROMPT = PromptTemplate(TEXT_TO_SQL_TMPL)
    text_to_sql_prompt_string = TEXT_TO_SQL_PROMPT.format(question_string=question_string, relavent_table_info=relavent_table_info, reason_for_selecting_those_tables=reason_for_selecting_those_tables)

    #print(text_to_sql_prompt_string)

    output = sql_query_generation_llm.complete(text_to_sql_prompt_string)

    print(output)

    # extract values from response
    
    
    
    
    sql_queries_count = int(extract_value_from_response_string(output.text, 'SQL_Queries_Count'))

    sql_queries = []
    if sql_queries_count >= 1:
        sql_query_1 = extract_value_from_response_string(output.text, 'SQL_Query_1')
        sql_queries.append(sql_query_1)
    if sql_queries_count >= 2:
        sql_query_2 = extract_value_from_response_string(output.text, 'SQL_Query_2')
        sql_queries.append(sql_query_2)
    if sql_queries_count >= 3:
        sql_query_3 = extract_value_from_response_string(output.text, 'SQL_Query_3')
        sql_queries.append(sql_query_3)
    if sql_queries_count >= 4:
        sql_query_4 = extract_value_from_response_string(output.text, 'SQL_Query_4')
        sql_queries.append(sql_query_4)


    print(sql_queries)


    return {
        'sql_queries': sql_queries,
    }