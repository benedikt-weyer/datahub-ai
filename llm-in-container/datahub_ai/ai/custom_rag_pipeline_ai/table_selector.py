from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

def select_important_tables(query_string, table_info, table_selector_llm: Ollama):

    SELECT_TABLE_TMPL = (
        "Select 0 to 4 tables that should be used in a sql query to answer the question \n"
        "Please also evaluate if an sql query is in general necessary to answer the question \n"
        "When you select at least one table then also provide a reason for selecting those tables \n"
        "Here is the data you need: \n"
        "Question: {query_string}\n"
        "Table Info: {table_info}\n"
        "\n\n"
        "Format your response as stated below, each taking one line: \n"
        "Is_SQL_Query_Necessary: true or false \n"
        "Selected_Tables: table_name_1, table_name2... \n"
        "Reason_For_Selecting_Those_Tables: The reason for selecting the tables here, when necessary. Else leave empty \n"
    )
    SLECT_TABLE_PROMPT = PromptTemplate(SELECT_TABLE_TMPL)
    select_table_prompt_string = SLECT_TABLE_PROMPT.format(query_string=query_string, table_info=table_info)

    output = table_selector_llm.complete(select_table_prompt_string)

    print(output)

    # extract values from response
    is_sql_query_necessary = extract_value_from_response_string(output.text, 'SQL_Query_Necessary')
    selected_tables = extract_value_from_response_string(output.text, 'Selected_Tables')



    return {
        'is_sql_query_necessary': is_sql_query_necessary,
        'relavant_tables': selected_tables
    }