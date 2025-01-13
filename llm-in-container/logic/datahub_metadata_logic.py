import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_access import datahub_tables_access as dta

from pprint import pprint as pp


def get_datahub_tables_metadata():
    
    datahub_data = dta.get_datahub_tables()
    
    table_data_in_string_format = list(str)
    print(datahub_data[2])
    
    return

get_datahub_tables_metadata()