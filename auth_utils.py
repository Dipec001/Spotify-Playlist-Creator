import json

# Example function to save token to a file
def save_token_to_file(token, filename):
    with open(filename, 'w') as file:
        json.dump(token, file)

# Example function to read token from a file
def read_token_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)
