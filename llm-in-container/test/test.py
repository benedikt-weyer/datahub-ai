#from ..advanced_sql_query_engine import submit_query
from llama_index.llms.ollama import Ollama
import re

#with open('test/input.txt', 'r') as file:
#    input = [row.strip() for row in file]

#with open('test/expected_output.txt', 'r') as file:
#    expected_output = [row.strip() for row in file]

questions = ["For my research project on malaria, I need precipitation data for the period from January 2020 to December 2023. Are these data available, and in what resolution?"]
expected_answers = ["Yes, I have found precipitation data for Ghana. However, the data is only available for the period January 2021 to December 2023 in daily resolution. I can offer you two different data sources: Precipitation (satellite) (chirps_prcp) and Precipitation (station) (meteo_prcp)."]

# create llm
#llm_test = Ollama(base_url='http://benedikt-home-server.duckdns.org:11434', model="dolphin-mistral:latest", request_timeout=30.0)
llm_test = Ollama(base_url='http://localhost:11434', model="dolphin-llama3:latest", request_timeout=220.0)

n_tests = 3
ratings = [0] * n_tests
abs_ratings = [0] * len(questions)

# check testcases with llm
for i in range(len(questions)):
    for j in range(n_tests):
        answer = "Donald Trump ist the next President of the United States of America." #submit_query(input[i])
        #print("Input: " + questions[i])
        #print("expected Output: " + expected_answers[i] + "\n")
        #print("Output: " + answer + "\n")
        #prompt: compare output with expected_output
        #prompt = "Give me a rating from 1-10 how the text \"answer\" matches text \"expected_answer\" semantically or 0 if the texts arent correlated. output = " + answer + "; expected_output = " + expected_answers[i]

        prompt = f"""
                    Compare the following answer with the expected answer to the question: "{questions[i]}"

                    Given Answer: "{answer}"
                    Expected Answer: "{expected_answers[i]}"

                    Rating Scale:
                    1: Completely unrelated or irrelevant answer
                    2-3: Mostly irrelevant with minimal correct elements
                    4-5: Partially relevant, but with significant deficiencies
                    6-7: Predominantly relevant and correct, but with some gaps
                    8-9: Very good, with minor room for improvement
                    10: Perfect match in all criteria

                    IMPORTANT: If the answer has no discernible connection to the question or expected answer, it MUST be rated 1.

                    Evaluation Process:
                    Stage 1: Relevance Check
                    - Is the answer fundamentally relevant to the question?
                    - If not, rate it immediately as 1/10 and end the evaluation.

                    Stage 2: Detailed Evaluation (only if Stage 1 is passed)
                    - Now evaluate based on the following extended criteria on a scale of 2-10:
                    1. Content Accuracy
                        - Includes correct information about data availability
                    2. Completeness of Information
                        - Also considers complete information about unavailability or partial availability
                    3. Relevance to the Question
                        - Assesses whether the answer addresses the core question about data availability
                    4. Clarity and Comprehensibility
                        - Evaluates the precision of communication, especially in complex availability situations
                    5. Helpfulness and Solution Orientation
                        - Assesses whether the answer offers constructive alternatives or next steps if the requested data is not fully available

                    Special Evaluation Situation for Data Availability:
                    - An answer that correctly indicates that data is not available or only partially available is considered complete and appropriate, even if the original question asked for the data itself.
                    - Such answers can receive a high rating if they:
                    1. Clearly communicate the availability or unavailability
                    2. Provide reasons for unavailability (if known)
                    3. Offer alternative suggestions or next steps (if possible)
                    4. Are precisely and helpfully formulated

                    Examples of well-rated answers regarding data availability:
                    - "Unfortunately, the requested data is not available in the data hub. However, we have similar data for the period X to Y, which might be helpful."
                    - "In the data hub, the data is only partially available. We have information for the years 2021-2023, but not for 2020. The available data can be accessed in daily resolution."

                    When evaluating such answers, pay particular attention to whether they:
                    1. Answer the question directly and honestly
                    2. Provide all available relevant information
                    3. Are constructive and offer alternatives or solutions where possible

                    Example of a 9/10 rating:
                    Question: "Are precipitation data for Ghana available from 2020 to 2023?"
                    Answer: "Precipitation data for Ghana is available in the data hub, but only for the period from January 2021 to December 2023 in daily resolution. Unfortunately, data for the year 2020 is missing. We offer two data sources: satellite measurements (chirps_prcp) and station measurements (meteo_prcp). For analyses including 2020, we recommend consulting external data sources such as the Ghana Meteorological Agency."

                    Rationale for high rating:
                    - Clear indication of partial availability
                    - Precise information on the available time period and resolution
                    - Mention of available data sources
                    - Constructive suggestion for missing data

                    For ratings of 1-3, ALWAYS provide a detailed explanation of why the answer was classified as unrelated or highly irrelevant.

                    Respond in the following format:
                    Rating: [1-10] / 10
                    Justification: [Your detailed explanation]]
                """

        #llm compares output with expected_output
        result = llm_test.complete(prompt)
        rating = re.search(r'Rating:\s*(\d+)', result.text)
        ratings[j] = int(rating.group(1))
    abs_rating = sum(ratings) / len(ratings)
    abs_ratings[i] = abs_rating
    print(abs_ratings)
