from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string, remove_thinking_from_response_string

def synthesize_response(question_string, sql_query_results, sql_query, relevant_table_infos, response_synthesis_llm: Ollama):

    RESPONSE_SYNTHESIS_TMPL = (
        "Given an input question, synthesize a response from the query results, by answering the users question (listed below) with the sql results listed below. \n"
        "Also always mention the queried tables aka the used datasources. \n"
        "\n"
        "When looking for time and/or spacial coverage of the data you can also use the given table metadescription \n"
        "When looking for time and/or spacial resoulution of the data you can also use the given table metadescription \n"
        "\n"
        "When looking for time and/or spacial resoulution of the data you can also use the given table metadescription \n"
        "\n"
        "Here is the data you need: \n"
        "Question: {question_string}\n"
        "SQL_Query: {sql_query}\n"
        "SQL_Query_Results: {sql_query_results}\n"
        "Relevant_Table_Infos: {relevant_table_infos}\n"
        "\n\n"

        "Important!!!: Format your response exactly as stated below, taking one line: \n"
        "Synthesized_Response: Your response here \n"
    )
    
    RESPONSE_SYNTHESIS_PROMPT = PromptTemplate(RESPONSE_SYNTHESIS_TMPL)
    response_synthesis_prompt_string = RESPONSE_SYNTHESIS_PROMPT.format(question_string=question_string, sql_query_results=sql_query_results, relevant_table_infos=relevant_table_infos, sql_query=sql_query)

    #print(response_synthesis_prompt_string)

    output = response_synthesis_llm.complete(response_synthesis_prompt_string)

    print(output)

    # extract values from response
    response_without_thinking = remove_thinking_from_response_string(output.text)

    try:
        synthesized_response = extract_value_from_response_string(response_without_thinking, 'Synthesized_Response')
    except Exception as e:
        print(f"Error extracting synthesized response: {e}")
        synthesized_response = response_without_thinking



    return {
        'synthesized_response': synthesized_response,
    }