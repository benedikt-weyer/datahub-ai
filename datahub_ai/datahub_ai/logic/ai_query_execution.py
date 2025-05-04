from datahub_ai.data_access import datahub_tables_access

def execute_generated_query(sql_query):
    return datahub_tables_access.execute_generated_query(sql_query)
