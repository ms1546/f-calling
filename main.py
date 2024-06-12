import openai
import json

openai.api_key = ""

functions = [
    {
        "name": "extract_information",
        "description": "Extracts dates, times, places, and people from a given text",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract information from"
                }
            },
            "required": ["text"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Extract information from the following text: 'John Doe met Jane Smith at Central Park on 2023-04-01 at 14:30.'"}
    ],
    functions=functions,
    function_call="auto"
)

function_call = response.choices[0].message.get("function_call")
if function_call:
    function_name = function_call["name"]
    arguments = json.loads(function_call["arguments"])

    if function_name == "extract_information":
        text = arguments["text"]
        result = extract_information(text)
        print(f"Extracted information: {result}")

def extract_information(text):
    import re
    from datetime import datetime

    date_pattern = r'\b(\d{4}-\d{1,2}-\d{1,2})\b'
    time_pattern = r'\b(\d{1,2}:\d{2})\b'
    place_pattern = r'\b(?:in|at|near|on)\s([A-Z][a-z]+)\b'
    person_pattern = r'\b([A-Z][a-z]+\s[A-Z][a-z]+)\b'

    dates = re.findall(date_pattern, text)
    times = re.findall(time_pattern, text)
    places = re.findall(place_pattern, text)
    people = re.findall(person_pattern, text)

    return {
        "dates": dates,
        "times": times,
        "places": places,
        "people": people
    }
