#from ..advanced_sql_query_engine import submit_query
from llama_index.llms.ollama import Ollama

#with open('test/input.txt', 'r') as file:
#    input = [row.strip() for row in file]

#with open('test/expected_output.txt', 'r') as file:
#    expected_output = [row.strip() for row in file]

questions = ["For my research project on malaria, I need precipitation data for the period from January 2020 to December 2023. Are these data available, and in what resolution?"]
expected_answers = ["Thank you for your question. Yes, I have found precipitation data for Ghana. However, the data is only available for the period January 2021 to December 2023 in daily resolution. I can offer you two different data sources: Precipitation (satellite) (chirps_prcp) and Precipitation (station) (meteo_prcp)."]

# create llm
#llm_test = Ollama(base_url='http://benedikt-home-server.duckdns.org:11434', model="dolphin-mistral:latest", request_timeout=30.0)
llm_test = Ollama(base_url='http://localhost:11434', model="dolphin-llama3:latest", request_timeout=220.0)


# check testcases with llm
for i in range(len(questions)):
    answer = "Hello World" #submit_query(input[i])
    print("Input: " + questions[i])
    print("expected Output: " + expected_answers[i])
    print("Output: " + answer)
    #vergleiche output mit expected_output
    prompt = "Give me a rating from 1-10 how the text \"answer\" matches text \"expected_answer\" semantically or 0 if the texts arent correlated. output = " + answer + "; expected_output = " + expected_answers[i]
    #llm den prompt übergeben und Antwort printen
    result = llm_test.complete(prompt)
    print(result)
