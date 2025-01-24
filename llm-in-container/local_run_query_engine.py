#from advanced_sql_query_engine import submit_query
from datahub_ai.logic.datahub_metadata_logic import get_datahub_tables_metadata
from datahub_ai.ai.custom_rag_pipeline_ai import ai_engine
from llama_index.core.base.llms.types import ChatMessage

#print(get_datahub_tables_metadata(without_docker_flag=True))
#response = submit_query("What districts are in the data?", True)
#response = submit_query("How was the percipitation in Korle Klottey Municipal in 2020?", True)
#response = submit_query("How was the percipitation in Korle Klottey Municipal in 2020?", True, 'http://localhost:11434')

#print(response)

output = ai_engine.submit_query("How are you today?", is_verbose=True, without_docker=True)
print(output['response'])
chat_history = [ChatMessage(**message) for message in output['chat_history']]
print(chat_history[0])


# output = ai_engine.submit_query("How was the percipitation in Ashanti in 2020?", is_verbose=True, without_docker=True)
# print("##Response:")
# print(output['response'])

# print("-------------------")


# output = ai_engine.submit_query("For my research project on malaria, I need precipitation data for the period from January 2020 to December 2023. Are these data available, and in what resolution?", is_verbose=True, without_docker=True)
# print("##Response:")
# print(output['response'])

# print("-------------------")

# output = ai_engine.submit_query("I need the location of all schools in Kumasi district, Ghana. Is this dataset available?", is_verbose=True, without_docker=True)
# print("##Response:")
# print(output['response'])

# print("-------------------")

# output = ai_engine.submit_query("I need a quick overview of the Ada East district, Ghana. How large is this district, how many people live there, and what is the most recent urbanization rate?", is_verbose=True, without_docker=True)
# print("##Response:")
# print(output['response'])

# print("-------------------")

