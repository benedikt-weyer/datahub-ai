from data_access import data_description_access, datahub_tables_access


def get_inactive_table_names():
    # get all tables from datahub
    table_names = datahub_tables_access.get_table_names()

    # get all active tables from mongo db
    active_tables = data_description_access.get_active_tables()

    active_table_names = [table['table_name'] for table in active_tables]

    inactive_table_names = [table_name for table_name in table_names if table_name not in active_table_names]

    return inactive_table_names


def get_active_tables():
    # get all active tables from mongo db
    active_tables = data_description_access.get_active_tables()

    return active_tables


# def get_active_tables_for_ai():
#     # get all active tables from mongo db
#     active_tables = data_description_access.get_active_tables()

#     #format them for AI
#     active_tables = [{"table_name": table['table_name'], "table_description": table['table_description']} for table in active_tables]

#     return active_tables


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
