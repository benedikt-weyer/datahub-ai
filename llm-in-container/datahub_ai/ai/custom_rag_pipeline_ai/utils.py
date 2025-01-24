import re

def extract_value_from_response_string(response_string, key):
    """
    Extracts the value associated with a specified key from a response string.

    Args:
        response_string (str): The response string to search within.
        key (str): The key whose associated value is to be extracted.

    Returns:
        str: The value associated with the specified key.

    Raises:
        ValueError: If the key is not found in the response string or if no 
                    value is associated with the key.
    """
    # Append ':' to the key
    key_with_colon = key + ':'
    
    # Find the start index of the key in the response string
    key_start = response_string.find(key_with_colon)
    if key_start == -1:
        raise ValueError(f"Key '{key}' not found in response string.")
    
    # Find the end index of the key in the response string
    key_end = response_string.find("\n", key_start)
    if key_end == -1:
        key_end = len(response_string)
    
    # Extract the value associated with the key
    value = response_string[key_start + len(key_with_colon):key_end].strip()
    
    return value


def remove_thinking_from_response_string(response_string):
    # Define the pattern to match <think>...</think> tags
    pattern = re.compile(r'<think>.*?</think>', re.DOTALL)

    # Remove the matched patterns from the response string
    cleaned_response = re.sub(pattern, '', response_string)

    return cleaned_response.strip()