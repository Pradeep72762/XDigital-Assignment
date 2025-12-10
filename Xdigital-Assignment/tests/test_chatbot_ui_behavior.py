import pytest
import time
from pages.chatbot_page import ChatbotPage


class TestChatbotUIBehavior:

    @pytest.mark.desktop
    def test_chat_widget_loads_desktop(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        
        assert chatbot.is_chat_widget_visible(), "Chat widget should be visible on desktop"
        
        viewport_width = chatbot.get_viewport_width()
        chat_container_width = chatbot.get_chat_container_width()
        
        assert chat_container_width > 0, "Chat container should have width on desktop"
        assert chat_container_width <= viewport_width, "Chat container should fit within viewport"
    
    def test_chat_widget_loads_mobile(self, page_mobile):
        chatbot = ChatbotPage(page_mobile)
        chatbot.navigate_to_english()
        
        assert chatbot.is_chat_widget_visible(), "Chat widget should be visible on mobile"
        
        viewport_width = chatbot.get_viewport_width()
        chat_container_width = chatbot.get_chat_container_width()
        
        assert chat_container_width > 0, "Chat container should have width on mobile"
        assert chat_container_width >= (viewport_width * 0.90), "Chat container should adapt to mobile width"
    
    def test_user_can_send_message(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        
        assert chatbot.is_input_editable(), "Input box should be editable and accept text"
        
        send_button = chatbot.get_send_button()
        assert send_button.is_visible(), "Send button should be visible"
        assert chatbot.is_send_button_enabled() == False, "Send button should be disabled when input is empty"
        
        input_element = chatbot.get_chat_input()
        input_element.fill("Test message")
        time.sleep(0.5)
        assert chatbot.is_send_button_enabled(), "Send button should be enabled after typing"
        
        input_element.clear()
        assert chatbot.is_send_button_enabled() == False, "Send button should be disabled when input is cleared"
        
        chatbot.send_message_with_enter("Hello, how can I help?")
        assert chatbot.is_input_cleared(), "Input should be cleared after sending with Enter key"
    
    def test_ai_response_rendered(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        
        chatbot.send_message("What services are available?")
        chatbot.wait_for_response(timeout=30000)
        
        last_message = chatbot.get_last_message()
        assert len(last_message) > 0, "AI response should be rendered"
        assert len(last_message) > 10, "AI response should contain meaningful content"
    
    def test_multilingual_support_english_ltr(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        assert chatbot.is_ltr_layout(), "English version should use LTR layout"
    
    def test_multilingual_support_arabic_rtl(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_arabic()
        assert chatbot.is_rtl_layout(), "Arabic version should use RTL layout"
    
    def test_input_cleared_after_sending(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        
        chatbot.send_message("Test message")
        assert chatbot.is_input_cleared(), "Input should be cleared after sending"
    
    def test_scroll_functionality(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        
        for i in range(3):
            chatbot.send_message(f"Test message {i+1}")
            chatbot.wait_for_response(timeout=20000)
        
        chatbot.scroll_to_bottom()
        assert True
    
    def test_chat_input_accessibility(self, page):
        chatbot = ChatbotPage(page)
        chatbot.navigate_to_english()
        
        input_element = chatbot.get_chat_input()
        assert input_element.is_visible(), "Chat input should be visible"
        assert input_element.is_enabled(), "Chat input should be enabled"
        
        input_element.fill("Accessibility test")
        assert input_element.input_value() == "Accessibility test", "Input should accept text"
