#from ..advanced_sql_query_engine import submit_query
from llama_index.llms.ollama import Ollama
import re
import requests
import json

def read_test_data_from_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    
    questions = [item['question'] for item in data['test_data'] if item['id'] != -1] 
    expected_answers = [item['expected_answer'] for item in data['test_data'] if item['id'] != -1] 
    
    return questions, expected_answers

def read_file(path):
    with open(path, 'r') as file:
        lines = [row.strip() for row in file]
    return lines

def test_questions(llm_test, questions, expected_answers):
    n_tests = 3
    ratings = [0] * n_tests
    abs_ratings = [0] * len(questions)
    ratings_for_milestone_4 = [0] * n_tests * len(questions)

    print("testing " + str(len(questions)) + " questions with " + str(n_tests) + " runs per question...")


    for i in range(len(questions)):

        for j in range(n_tests):

            print("testing question nr " + str(i) + ", run nr " + str(j) + "...")

            

            url = 'http://localhost:8001/api/query'
            #url = 'http://localhost:8000/ai-chat'
            payload = { 'query': questions[i] }
            headers = {"Content-Type": "application/json; charset=utf-8"}

            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                answer = response.json().get('response', 'No response field in JSON')
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                answer = 'Error: Request failed'
            except ValueError:
                print("Error: Unable to parse JSON response")
                answer = 'Error: Invalid JSON response'

            print(answer)

            prompt = f"""
                        Compare the following answer with the expected answer to the question: "{questions[i]}"

                        Given Answer: "{answer}"
                        Expected Answer: "{expected_answers[i]}"

                        Rating Scale:
                        1: Completely unrelated or irrelevant answer
                        2-15: Mostly irrelevant with minimal correct elements
                        16-50: Partially relevant, but with significant deficiencies
                        60-70: Predominantly relevant and correct, but with some gaps
                        80-90: Very good, with minor room for improvement
                        100: Perfect match in all criteria

                        IMPORTANT: If the answer has no discernible connection to the question or expected answer, it MUST be rated 1.

                        Evaluation Process:
                        Stage 1: Relevance Check
                        - Is the answer fundamentally relevant to the question?
                        - If not, rate it immediately as 1/100 and end the evaluation.

                        Stage 2: Detailed Evaluation (only if Stage 1 is passed)
                        - Now evaluate based on the following extended criteria on a scale of 20-100:
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

                        Example of a 90/100 rating:
                        Question: "Are precipitation data for Ghana available from 2020 to 2023?"
                        Answer: "Precipitation data for Ghana is available in the data hub, but only for the period from January 2021 to December 2023 in daily resolution. Unfortunately, data for the year 2020 is missing. We offer two data sources: satellite measurements (chirps_prcp) and station measurements (meteo_prcp). For analyses including 2020, we recommend consulting external data sources such as the Ghana Meteorological Agency."

                        Rationale for high rating:
                        - Clear indication of partial availability
                        - Precise information on the available time period and resolution
                        - Mention of available data sources
                        - Constructive suggestion for missing data

                        For ratings of 10-30, ALWAYS provide a detailed explanation of why the answer was classified as unrelated or highly irrelevant.

                        Respond in the following format:
                        Rating: [1-100] / 100
                        Justification: [Your detailed explanation]]
                    """

            #llm compares output with expected_output
            result = llm_test.complete(prompt)
            rating = re.search(r'Rating:\s*(\d+)', result.text)
            ratings[j] = int(rating.group(1))
            ratings_for_milestone_4[i*n_tests+j] = int(rating.group(1))

        abs_rating = sum(ratings) / len(ratings)
        abs_ratings[i] = round(abs_rating,2)

    print("testing complete!")
    #return abs_ratings
    return ratings_for_milestone_4

def print_result(ratings):
    print("ratings: " + str(ratings))
    print("average rating: " + str(round(sum(ratings)/len(ratings),2)))

def save_result(ratings, filename='ratings.md'):
    with open(filename, 'w') as md_file:
        for index, rating in enumerate(ratings, start=0):
            md_file.write(f'question-id: {index}, rating: {rating:.2f}\n')


#read questions and answers
#questions = read_file("./evaluate-ai/questions.txt")
#expected_answers = read_file("./evaluate-ai/expected_answers.txt")
questions, expected_answers = read_test_data_from_json("./evaluate-ai/test_data.json")

# create llm
llm_test = Ollama(base_url='http://openmain.de:11434', model="dolphin-mistral:latest", request_timeout=30.0)
#llm_test = Ollama(base_url='http://localhost:11434', model="dolphin-llama3:latest", request_timeout=220.0)

# check testcases with llm
ratings = test_questions(llm_test=llm_test, questions=questions, expected_answers=expected_answers)
print_result(ratings=ratings)
save_result(ratings=ratings)
