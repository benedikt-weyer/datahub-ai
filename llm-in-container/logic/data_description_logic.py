from data_access import data_description_access, datahub_tables_access


def get_inactive_table_names():
    # get all tables from datahub
    table_names = datahub_tables_access.get_table_names()

    # get all active tables from mongo db
    active_tables = data_description_access.get_active_table_names()

    active_table_names = [table['table_name'] for table in active_tables]

    inactive_table_names = [table_name for table_name in table_names if table_name not in active_table_names]

    return inactive_table_names