from playwright.sync_api import Page
import time


class ChatbotPage:
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://ask.u.ae"
        
    def navigate_to_english(self):
        self.page.goto(f"{self.base_url}/en/uask")
        self.page.wait_for_load_state("networkidle")
        self._handle_disclaimer()
        self._handle_recaptcha()
        
    def navigate_to_arabic(self):
        self.page.goto(f"{self.base_url}/ar/uask")
        self.page.wait_for_load_state("networkidle")
        self._handle_disclaimer()
        self._handle_recaptcha()
    
    def _handle_disclaimer(self):
        try:
            accept_button = self.page.locator('button[aria-label="Accept and continue"]')
            if accept_button.is_visible(timeout=3000):
                accept_button.click()
                self.page.wait_for_timeout(1000)
        except Exception:
            pass
    
    def _handle_recaptcha(self, max_wait: int = 300):
        try:
            self.page.wait_for_timeout(2000)
            recaptcha_detected = False
            
            try:
                if self.page.locator('#rc-imageselect').is_visible(timeout=2000):
                    recaptcha_detected = True
            except Exception:
                pass
            
            try:
                if self.page.locator('.recaptcha-checkbox-checkmark').is_visible(timeout=2000):
                    recaptcha_detected = True
            except Exception:
                pass
            
            try:
                if self.page.locator('div.grecaptcha-badge').is_visible(timeout=2000):
                    recaptcha_detected = True
            except Exception:
                pass
            
            try:
                if self.page.locator('iframe[title="reCAPTCHA"]').is_visible(timeout=2000):
                    recaptcha_detected = True
            except Exception:
                pass
            
            try:
                if self.page.locator('iframe[src*="recaptcha"]').is_visible(timeout=2000):
                    recaptcha_detected = True
            except Exception:
                pass
            
            try:
                chat_input = self.page.locator('textarea#conversation')
                if chat_input.is_visible(timeout=3000) and not chat_input.is_enabled():
                    recaptcha_detected = True
            except Exception:
                pass
            
            if recaptcha_detected:
                print(f"\n{'='*70}")
                print(f"[INFO] reCAPTCHA DETECTED!")
                print(f"[INFO] Waiting up to {max_wait} seconds ({max_wait//60} minutes) for manual resolution...")
                print(f"[INFO] Please solve the reCAPTCHA in the browser window.")
                print(f"{'='*70}\n")
                
                start_time = time.time()
                elapsed = 0
                last_progress = 0
                
                while elapsed < max_wait:
                    try:
                        challenge_dialog = self.page.locator('#rc-imageselect')
                        if not challenge_dialog.is_visible(timeout=1000):
                            chat_input = self.page.locator('textarea#conversation')
                            if chat_input.is_visible(timeout=1000) and chat_input.is_enabled():
                                elapsed = int(time.time() - start_time)
                                print(f"\n[SUCCESS] reCAPTCHA resolved after {elapsed} seconds!")
                                time.sleep(3)
                                return
                    except Exception:
                        try:
                            chat_input = self.page.locator('textarea#conversation')
                            if chat_input.is_visible(timeout=1000) and chat_input.is_enabled():
                                elapsed = int(time.time() - start_time)
                                print(f"\n[SUCCESS] reCAPTCHA resolved after {elapsed} seconds!")
                                time.sleep(3)
                                return
                        except Exception:
                            pass
                    
                    elapsed = int(time.time() - start_time)
                    if elapsed - last_progress >= 30:
                        remaining = max_wait - elapsed
                        minutes = remaining // 60
                        seconds = remaining % 60
                        print(f"[WAITING] Still waiting for reCAPTCHA... {elapsed}s elapsed, {minutes}m {seconds}s remaining...")
                        last_progress = elapsed
                    
                    time.sleep(2)
                
                print(f"\n[WARNING] reCAPTCHA wait time ({max_wait}s) exceeded!")
        except Exception:
            pass
        
    def is_chat_widget_visible(self) -> bool:
        try:
            chat_input = self.page.locator('textarea#conversation')
            if chat_input.is_visible(timeout=5000):
                return True
            chat_component = self.page.locator('chat')
            return chat_component.is_visible(timeout=2000)
        except Exception:
            return False
    
    def open_chat_widget(self):
        try:
            chat_button = self.page.locator('button.chat-button[aria-label="Open Chat History"]')
            if chat_button.is_visible(timeout=3000):
                chat_button.click()
                time.sleep(1)
        except Exception:
            pass
    
    def get_chat_input(self):
        chat_input = self.page.locator('textarea#conversation')
        if chat_input.is_visible(timeout=5000):
            return chat_input
        raise Exception("Chat input field not found")
    
    def send_message(self, message: str):
        input_element = self.get_chat_input()
        input_element.fill(message)
        input_element.press("Enter")
        time.sleep(2)
        
        self._handle_recaptcha(max_wait=300)
        
        try:
            current_value = input_element.input_value()
            if current_value.strip() == message.strip():
                time.sleep(2)
                current_value = input_element.input_value()
                if current_value.strip() == message.strip():
                    print("[INFO] Message may not have been sent due to reCAPTCHA. Retrying...")
                    input_element.press("Enter")
                    time.sleep(2)
        except Exception:
            pass
        
        self._handle_recaptcha(max_wait=300)
    
    def is_input_cleared(self) -> bool:
        try:
            input_element = self.get_chat_input()
            value = input_element.input_value()
            return value.strip() == ""
        except Exception:
            return False
    
    def is_input_editable(self) -> bool:
        try:
            input_element = self.get_chat_input()
            if not input_element.is_visible() or not input_element.is_enabled():
                return False
            test_text = "test"
            input_element.fill(test_text)
            result = input_element.input_value() == test_text
            input_element.clear()
            return result
        except Exception:
            return False
    
    def get_send_button(self):
        return self.page.locator('button[aria-label="Send Message"]').first
    
    def is_send_button_enabled(self) -> bool:
        try:
            send_button = self.get_send_button()
            if not send_button.is_visible(timeout=3000):
                return False
            time.sleep(0.3)
            return not send_button.is_disabled()
        except Exception:
            return False
    
    def send_message_with_enter(self, message: str):
        input_element = self.get_chat_input()
        input_element.fill(message)
        input_element.press("Enter")
        time.sleep(2)
        self._handle_recaptcha(max_wait=300)
    
    def wait_for_response(self, timeout: int = 30000):
        max_wait = timeout / 1000
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            try:
                ai_messages = self.page.locator('div.chatContainer div.card-body')
                if ai_messages.count() > 0:
                    last_ai_message = ai_messages.last
                    if last_ai_message.is_visible(timeout=1000):
                        text = last_ai_message.inner_text().strip()
                        if text and len(text) > 10:
                            time.sleep(1)
                            return
            except Exception:
                pass
            time.sleep(2)
    
    def get_last_message(self) -> str:
        for attempt in range(10):
            try:
                self.page.wait_for_timeout(2000)
                ai_messages = self.page.locator('div.chatContainer div.card-body')
                
                if ai_messages.count() > 0:
                    last_ai_message = ai_messages.last
                    if last_ai_message.is_visible(timeout=3000):
                        text = last_ai_message.inner_text().strip()
                        if text and len(text) > 0:
                            return text
                
                chat_container = self.page.locator('div[role="listbox"][aria-label="Messages"]')
                if chat_container.is_visible(timeout=2000):
                    all_ai_messages = chat_container.locator('div[role="option"].card-body')
                    if all_ai_messages.count() > 0:
                        last_message = all_ai_messages.last
                        if last_message.is_visible(timeout=2000):
                            text = last_message.inner_text().strip()
                            if text and len(text) > 0:
                                return text
            except Exception:
                pass
            
            if attempt < 9:
                time.sleep(3)
        
        return ""
    
    def get_all_messages(self) -> list:
        try:
            message_elements = self.page.locator('div.chatContainer div[class*="message"]').all()
            return [msg.inner_text() for msg in message_elements if msg.is_visible()]
        except Exception:
            return []
    
    def is_rtl_layout(self) -> bool:
        try:
            body = self.page.locator("body")
            direction = body.evaluate("el => window.getComputedStyle(el).direction")
            return direction == "rtl"
        except Exception:
            return self.page.locator("html[dir='rtl']").count() > 0
    
    def is_ltr_layout(self) -> bool:
        try:
            body = self.page.locator("body")
            direction = body.evaluate("el => window.getComputedStyle(el).direction")
            return direction == "ltr"
        except Exception:
            return self.page.locator("html[dir='ltr']").count() > 0 or self.page.locator("html:not([dir])").count() > 0
    
    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
    
    def can_scroll(self) -> bool:
        scroll_height = self.page.evaluate("document.body.scrollHeight")
        client_height = self.page.evaluate("document.documentElement.clientHeight")
        return scroll_height > client_height
    
    def check_loading_state(self) -> bool:
        try:
            loading = self.page.locator('[class*="loading"], [class*="spinner"]').first
            return loading.is_visible(timeout=1000)
        except Exception:
            return False
    
    def get_chat_container_width(self) -> int:
        try:
            chat_container = self.page.locator('div[role="listbox"][aria-label="Messages"]').first
            if chat_container.is_visible(timeout=5000):
                chat_container.scroll_into_view_if_needed()
                self.page.wait_for_timeout(500)
                box = chat_container.bounding_box()
                if box and box.get('width') and box['width'] > 0:
                    return int(box['width'])
            
            chat_container = self.page.locator('div.chatContainer').first
            if chat_container.is_visible(timeout=3000):
                chat_container.scroll_into_view_if_needed()
                self.page.wait_for_timeout(500)
                box = chat_container.bounding_box()
                if box and box.get('width') and box['width'] > 0:
                    return int(box['width'])
            
            chat_wrapper = self.page.locator('chat-wrapper-component').first
            if chat_wrapper.is_visible(timeout=3000):
                chat_wrapper.scroll_into_view_if_needed()
                self.page.wait_for_timeout(500)
                box = chat_wrapper.bounding_box()
                if box and box.get('width') and box['width'] > 0:
                    return int(box['width'])
            
            return 0
        except Exception:
            return 0
    
    def get_viewport_width(self) -> int:
        return self.page.viewport_size['width']

