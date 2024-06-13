import openai
import pytest
from main import extract_information

def test_openai_function_call():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは役立つアシスタントです。"},
            {"role": "user", "content": "次のテキストから情報を抽出してください: 'ジョン・ドウが2023年4月1日の14:30にセントラルパークでジェーン・スミスに会いました。'"}
        ],
        functions=functions,
        function_call="auto"
    )

    function_call = response.choices[0].message.get("function_call")
    assert function_call is not None, "Function call is None"

    function_name = function_call["name"]
    assert function_name == "extract_information", f"Expected function name 'extract_information', but got {function_name}"

    arguments = json.loads(function_call["arguments"])
    text = arguments["text"]

    expected_result = {
        "dates": ["2023-04-01"],
        "times": ["14:30"],
        "places": ["Central"],
        "people": ["John Doe", "Jane Smith"]
    }
    assert extract_information(text) == expected_result, f"Expected {expected_result}, but got {extract_information(text)}"
