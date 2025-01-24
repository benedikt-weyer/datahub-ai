from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

def select_important_tables(query_string, table_info, table_selector_llm: Ollama):

    SELECT_TABLE_TMPL = (
        "Instructions: \n"
        "Select 0 to 4 tables that should be used in a sql query to answer the provided question \n"
        "Please also evaluate if an sql query is in general necessary to answer the question, because we want to avoid making unnecessary requests \n"
        "The question can maybe be answered just with the help of the provided table metadescription, so please evaluate this carefully \n"
        "When you select at least one table, then also provide a reason for selecting those tables \n"
        "You can include the queried results. \n"
        # "When looking for time and/or spatial coverage of the data, you can also use the table metadescription, so you don't need an sql query \n"
        # "When looking for time and/or spatial resolution of the data, you can also use the table metadescription, so you don't need an sql query \n"
        "\n\n"
        "## Here is the data you need: \n"
        "### Question (refer to it): {query_string}\n"
        "### Table Info: {table_info}\n"
        # """Table Relations:
        # datalayers_datalayer	datalayers_datalayer_category_id_81fb48d0_fk_datalayer	FOREIGN KEY (category_id) REFERENCES datalayers_category(id) DEFERRABLE INITIALLY DEFERRED
        # shapes_shape	shapes_shape_parent_id_105bde46_fk_shapes_shape_id	FOREIGN KEY (parent_id) REFERENCES shapes_shape(id) DEFERRABLE INITIALLY DEFERRED
        # shapes_shape	shapes_shape_type_id_cfd28982_fk_shapes_type_id	FOREIGN KEY (type_id) REFERENCES shapes_type(id) DEFERRABLE INITIALLY DEFERRED
        # """
        "\n\n"
        "## Format your response exactly as stated below: \n"
        "Is_SQL_Query_Necessary: true or false \n"
        "Selected_Tables: table_name_1, table_name_2... \n"
        "Reason_For_Selecting_Those_Tables: The reason for selecting the tables here, when necessary. Else leave empty \n"
    )
    SLECT_TABLE_PROMPT = PromptTemplate(SELECT_TABLE_TMPL)
    select_table_prompt_string = SLECT_TABLE_PROMPT.format(query_string=query_string, table_info=table_info)
    print(select_table_prompt_string)
    output = table_selector_llm.complete(select_table_prompt_string)

    print(output)

    # extract values from response
    is_sql_query_necessary = extract_value_from_response_string(output.text, 'SQL_Query_Necessary')
    is_sql_query_necessary_bool = True if is_sql_query_necessary == 'true' else False

    selected_tables = extract_value_from_response_string(output.text, 'Selected_Tables')

    try:
        reason_for_selecting_those_tables = extract_value_from_response_string(output.text, 'Reason_For_Selecting_Those_Tables')
    except Exception as e:
        print(f"Error extracting reason for selecting tables: {e}")
        reason_for_selecting_those_tables = "no reason provided"



    return {
        'is_sql_query_necessary': is_sql_query_necessary_bool,
        'relavant_tables': selected_tables,
        'reason_for_selecting_those_tables': reason_for_selecting_those_tables
    }