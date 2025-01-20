import sys
import os

# Add the project root directory to PYTHONPATH
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datahub_ai.data_access.datahub_tables_access import get_datahub_table_metadata 

from pprint import pprint as pp


def get_datahub_tables_metadata(without_docker_flag=False):
    
    datahub_data = get_datahub_table_metadata(without_docker = without_docker_flag)
    
    pp(datahub_data)
    table_data_in_string_format = list()
    
    for table in sorted(datahub_data, key=lambda table: table["id"]):
        if table["description"].find("you can find follow up") != -1:
            table["description"] =  'not available'
        if table['related_to'] == '':
           related= f"and it is not related to any tables. "
        else:
            related = f" and it is related to following tables '{table['related_to']}'."
        
        description = (
        f"The table '{table['key']}' with the id {table['id']} belongs to the category '{table['category_name']}' and the category key is '{table['category_key']}'. "
        f"The contained information describes '{table['name']}', {related}. "
        f"The information this table provides is {table['description']}, measured in '{table['database_unit']}', "
        f"and the data coverage is {table['temporal_coverage']}."
        )
        print(description)
        table_data_in_string_format.append(description)
        
        
       
    return table_data_in_string_format
