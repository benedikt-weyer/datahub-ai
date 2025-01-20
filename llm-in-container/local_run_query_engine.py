#from advanced_sql_query_engine import submit_query
from datahub_ai.logic.datahub_metadata_logic import get_datahub_tables_metadata 

get_datahub_tables_metadata(without_docker_flag=True)
#response = submit_query("What districts are in the data?", True)
#response = submit_query("How was the percipitation in Korle Klottey Municipal in 2020?", True)
#response = submit_query("How was the percipitation in Korle Klottey Municipal in 2020?", True, 'http://localhost:11434')

#print(response)

while True:
    a=0