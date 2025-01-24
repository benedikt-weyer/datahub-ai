from datahub_ai.ai import advanced_sql_query_engine
from datahub_ai.ai.custom_rag_pipeline_ai import ai_engine

def query_ai(query_string, is_verbose=False):

    #result = advanced_sql_query_engine.submit_query(query_string, is_verbose) # old engine
    result = ai_engine.submit_query(query_string, is_verbose)

    return result