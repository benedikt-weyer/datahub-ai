from datahub_ai.data_access import data_description_access, datahub_tables_access


def get_inactive_table_names():
    # get all tables from datahub
    table_names = datahub_tables_access.get_table_names()

    # get all active tables from mongo db
    active_tables = data_description_access.get_active_tables()

    active_table_names = [table['table_name'] for table in active_tables]

    inactive_table_names = [table_name for table_name in table_names if table_name not in active_table_names]

    return inactive_table_names


def get_active_tables(without_docker=False):
    # get all active tables from mongo db
    active_tables = data_description_access.get_active_tables(without_docker).to_list()

    return active_tables



def add_table_without_description(table_name):
    # add table to active tables without description
    new_table = data_description_access.add_table(table_name, 'No description available')

    return new_table


def update_table(table_name, table_description):
    # update table description
    updated_table = data_description_access.update_table(table_name, table_description)

    return updated_table


def remove_table(table_name):
    # remove table from active tables
    removed_table = data_description_access.remove_table(table_name)

    return removed_table



def import_active_tables(file_data):
    # import active tables
    #imported_tables = data_description_access.import_active_tables(file_data)
    imported_tables = file_data.get('active_tables')

    # remove all old active tables
    data_description_access.remove_all_tables()

    # add new active tables
    for table in imported_tables:
        data_description_access.add_table(table['table_name'], table['table_description'])

    return imported_tables
