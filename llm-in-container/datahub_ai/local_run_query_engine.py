#from advanced_sql_query_engine import submit_query
from datahub_ai.ai.custom_rag_pipeline_ai import ai_engine

#response = submit_query("What districts are in the data?", True)
output = ai_engine.submit_query("How was the percipitation in Korle Klottey Municipal in 2020?", is_verbose=True, without_docker=True)
print(output['response'])
#response = submit_query("How was the percipitation in Korle Klottey Municipal in 2020?", True, 'http://localhost:11434')

#while True:
#    a=0