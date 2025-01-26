

def hydrate_response_with_datalayer_url(response_str, table_names):
    """
    Hydrate response string with datalayer url
    """
    hydrated_response_str = response_str
    for table_name in table_names:
        hydrated_response_str = hydrated_response_str.replace(table_name, f'<a href="/datalayers/{table_name}/">`{table_name}`</a>')

    return hydrated_response_str