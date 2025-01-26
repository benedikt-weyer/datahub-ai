import re



def hydrate_response_with_datalayer_url(response_str, table_names):
    """
    Hydrate response string with datalayer url
    """
    hydrated_response_str = response_str
    for table_name in table_names:
        pattern = re.compile(rf'`?{table_name}`?')
        hydrated_response_str = pattern.sub(f'<a href="/datalayers/{table_name}/" target="_blank">`{table_name}`</a>', hydrated_response_str)

    return hydrated_response_str