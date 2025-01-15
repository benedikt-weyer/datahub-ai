import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_access import datahub_tables_access as dta

from pprint import pprint as pp


def get_datahub_tables_metadata():
    
    datahub_data = dta.get_datahub_tables()
    
    table_data_in_string_format = list()
    
    for table in sorted(datahub_data, key=lambda table: table["id"]):
        if table["description"].find("you can find follow up") != -1:
            table["description"] =  'not available'
        description = (
        f"The table '{table['key']}' with the id {table['id']} belongs to the category '{table['category']}'. "
        f"The contained information describes '{table['name']}', and it is related to following tables {', '.join(table['related_to'])}. "
        f"The information this table provides is {table['description']}, measured in '{table['database_unit']}', "
        f"and the data coverage is {table['temporal_coverage']}."
        )
        table_data_in_string_format.append(description)
       
    return table_data_in_string_format

get_datahub_tables_metadata()