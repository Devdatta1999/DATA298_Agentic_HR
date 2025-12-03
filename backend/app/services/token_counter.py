import tiktoken
from typing import Dict, List


class TokenCounter:
    """Count tokens for LLM interactions"""
    
    def __init__(self):
        # Use cl100k_base encoding (used by GPT models, close approximation for Llama)
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string"""
        return len(self.encoding.encode(text))
    
    def count_tokens_in_messages(self, messages: List[Dict]) -> int:
        """Count total tokens in a list of messages"""
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                total += self.count_tokens(content)
            elif isinstance(content, dict):
                # Handle structured content
                for key, value in content.items():
                    if isinstance(value, str):
                        total += self.count_tokens(value)
        return total
    
    def get_token_usage(self, prompt: str, response: str) -> Dict[str, int]:
        """Get token usage breakdown"""
        prompt_tokens = self.count_tokens(prompt)
        response_tokens = self.count_tokens(response)
        total_tokens = prompt_tokens + response_tokens
        
        return {
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens
        }


token_counter = TokenCounter()


