from ai import advanced_sql_query_engine

def query_ai(query_string, is_verbose=False):

    result = advanced_sql_query_engine.submit_query(query_string, is_verbose)

    return result