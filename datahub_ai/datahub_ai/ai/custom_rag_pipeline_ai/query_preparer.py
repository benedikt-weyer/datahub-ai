from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

def prepare_query(query_string, chat_memory, query_preparer_llm: Ollama):

    PREPARE_QUERY_TMPL = (
        "Instructions: \n"
        "Please also evaluate if an sql query is in general necessary to answer the question, because we want to avoid making unnecessary requests. For that assume that every data is available in the database \n"
        "Also provide the language the question is in \n"
        "Also refine and enrich the question with the help of the given chat-memory. This is like the context for the question. Also make it understandable and don't lose any information. \n"
        "Also convert the question to English if it is not already in English \n"
        "\n\n"
        "## Here is the data you need: \n"
        "### Question: {query_string}\n"
        "### Chat_Memory: {chat_memory}\n"
        "\n\n"
        "## Format your response exactly as stated below: \n"
        "Is_SQL_Query_Necessary: true or false \n"
        "Language: Language the Querstion is in (e.g. German) \n"
        "Refined_Question: The refined and context enriched question \n"
    )
    PREPARE_QUERY_PROMPT = PromptTemplate(PREPARE_QUERY_TMPL)
    prepare_query_prompt_string = PREPARE_QUERY_PROMPT.format(query_string=query_string, chat_memory=chat_memory)
    print(prepare_query_prompt_string)
    output = query_preparer_llm.complete(prepare_query_prompt_string)

    print(output, flush=True)

    # extract values from response
    is_sql_query_necessary = extract_value_from_response_string(output.text, 'SQL_Query_Necessary')
    is_sql_query_necessary_bool = True if is_sql_query_necessary == 'true' else False

    language = extract_value_from_response_string(output.text, 'Language')

    refined_question = extract_value_from_response_string(output.text, 'Refined_Question')


    return {
        'is_sql_query_necessary': is_sql_query_necessary_bool,
        'language': language,
        'refined_question': refined_question
    }