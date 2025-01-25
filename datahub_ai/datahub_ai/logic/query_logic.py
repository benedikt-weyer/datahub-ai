from datahub_ai.ai.custom_rag_pipeline_ai import ai_engine

def query_ai(query_string, is_verbose=False, chat_store=None):

    result = ai_engine.submit_query(query_string, is_verbose=is_verbose, chat_store=chat_store)

    return result