from ..advanced_sql_query_engine import submit_query
from llama_index.llms.ollama import Ollama

with open('test/input.txt', 'r') as file:
    input = [row.strip() for row in file]

with open('test/expected_output.txt', 'r') as file:
    expected_output = [row.strip() for row in file]

# create llm
llm_test = Ollama(base_url='http://benedikt-home-server.duckdns.org:11434', model="dolphin-mistral:latest", request_timeout=30.0)

# check testcases with llm
for i in range(len(input)):
    output = "Hello World" #submit_query(input[i])
    print("Input: " + input[i])
    print("expected Output: " + expected_output[i])
    print("Output: " + output)
    #vergleiche output mit expected_output
    prompt = "Give me a rating from 1-10 how the text \"output\" matches text \"expected_output\" semantically. output = " + output + "; expected_output = " + expected_output
    #llm den prompt übergeben und Antwort printen
    answer = llm_test(prompt)
    print(answer)
