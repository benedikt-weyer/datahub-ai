def extract_value_from_response_string(response_string, key):
    key_start = response_string.find(key)
    if key_start == -1:
        raise ValueError(f"Key '{key}' not found in response string.")
    key_end = response_string.find("\n", key_start)
    if key_end == -1:
        key_end = len(response_string)
    value = response_string[key_start + len(key):key_end].strip()
    if not value:
        raise ValueError(f"No value found for key '{key}' in response string.")
    return value