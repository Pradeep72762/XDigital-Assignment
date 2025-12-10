import pytest
import json
import os
import time
from pages.chatbot_page import ChatbotPage
from ai_validator import AIValidator


def load_test_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "..", "data", "test_data.json")
    
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def chat_page(page):
    chatbot = ChatbotPage(page)
    chatbot.navigate_to_english()
    return chatbot


@pytest.mark.parametrize("test_case", load_test_data())
def test_ai_response_validation(chat_page, test_case):
    scenario = test_case["scenario"]
    prompt = test_case["prompt"]
    validation = test_case["validation"]
    
    print(f"\n[Scenario: {scenario}]")
    print(f"Prompt: {prompt}")
    
    chat_page.send_message(prompt)
    chat_page.wait_for_response(timeout=30000)
    time.sleep(3)
    
    actual_response = chat_page.get_last_message()
    print(f"Actual Response: {actual_response}")
    
    try:
        AIValidator.validate(actual_response, validation)
        print(f"[PASS] Validation passed for scenario: {scenario}")
    except AssertionError as e:
        print(f"[FAIL] Validation failed: {str(e)}")
        raise

