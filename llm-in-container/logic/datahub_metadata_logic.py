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
        print(table)
    
    return

get_datahub_tables_metadata()