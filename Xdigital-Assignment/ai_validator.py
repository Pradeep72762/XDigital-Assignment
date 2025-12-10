class AIValidator:
    
    @staticmethod
    def validate(response_text: str, criteria: dict) -> bool:
        normalized_text = response_text.lower()
        
        if "min_length" in criteria:
            min_length = criteria["min_length"]
            if len(response_text.strip()) < min_length:
                raise AssertionError(
                    f"Response too short. Expected at least {min_length} characters, "
                    f"got {len(response_text.strip())} characters. Response: '{response_text[:100]}...'"
                )
        
        if "must_contain" in criteria:
            missing_keywords = []
            for keyword in criteria["must_contain"]:
                if keyword.lower() not in normalized_text:
                    missing_keywords.append(keyword)
            
            if missing_keywords:
                raise AssertionError(
                    f"Missing required keywords: {', '.join(missing_keywords)}. "
                    f"Response: '{response_text[:200]}...'"
                )
        
        if "must_not_contain" in criteria:
            found_forbidden = []
            for keyword in criteria["must_not_contain"]:
                if keyword.lower() in normalized_text:
                    found_forbidden.append(keyword)
            
            if found_forbidden:
                raise AssertionError(
                    f"Found forbidden keywords: {', '.join(found_forbidden)}. "
                    f"Response should not contain these words. Response: '{response_text[:200]}...'"
                )
        
        return True

