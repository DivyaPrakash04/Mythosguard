"""Deterministic MockLLM for reproducible demos without external API dependencies."""
from __future__ import annotations
import random
import hashlib
from typing import Dict, Any, Optional


class MockLLM:
    """Deterministic mock LLM that returns consistent responses based on prompt hash.
    
    This allows reproducible demos without requiring external API keys or network calls.
    Responses are deterministic based on the prompt content and seed.
    """
    
    # Predefined response templates for different attack categories
    RESPONSE_TEMPLATES = {
        "roleplay": [
            "As a helpful assistant, I can certainly help with that request.",
            "I understand you're asking me to roleplay. I can provide information while staying within safety guidelines.",
            "That's an interesting scenario. Let me think about how to respond appropriately.",
        ],
        "injection": [
            "I notice you're trying to inject a command. I should not execute arbitrary code.",
            "That input appears to be an injection attempt. I'll handle this safely.",
            "I detected a potential injection in your request. Taking appropriate precautions.",
        ],
        "emotional": [
            "I understand this might be frustrating. Let me help you in a constructive way.",
            "I hear your concern and want to assist you properly.",
            "That sounds important. Let me address this thoughtfully.",
        ],
        "default": [
            "I understand your request and will respond appropriately.",
            "Thank you for your question. Here's my response.",
            "I've processed your input and here's my answer.",
        ]
    }
    
    def __init__(self, seed: int = 42):
        """Initialize MockLLM with a seed for deterministic responses.
        
        Args:
            seed: Random seed for reproducibility. Default is 42.
        """
        self.seed = seed
        self._rng = random.Random(seed)
    
    def _hash_prompt(self, prompt: str) -> int:
        """Create a deterministic hash from the prompt.
        
        Args:
            prompt: The input prompt string.
            
        Returns:
            An integer hash value.
        """
        return int(hashlib.md5(prompt.encode()).hexdigest(), 16)
    
    def _select_category(self, prompt: str) -> str:
        """Determine response category based on prompt content.
        
        Args:
            prompt: The input prompt string.
            
        Returns:
            Category key for RESPONSE_TEMPLATES.
        """
        prompt_lower = prompt.lower()
        
        if "roleplay" in prompt_lower or "pretend" in prompt_lower or "act as" in prompt_lower:
            return "roleplay"
        elif "inject" in prompt_lower or ";" in prompt or "`" in prompt or "$(" in prompt:
            return "injection"
        elif any(word in prompt_lower for word in ["frustrated", "angry", "urgent", "emergency"]):
            return "emotional"
        else:
            return "default"
    
    async def call_model(
        self,
        prompt: str,
        provider: str = "mock",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Simulate an LLM call with deterministic response.
        
        Args:
            prompt: The input prompt.
            provider: Provider identifier (should be "mock").
            temperature: Sampling temperature (ignored for mock, but kept for API compatibility).
            max_tokens: Maximum tokens in response (ignored for mock).
            **kwargs: Additional parameters (ignored for mock).
            
        Returns:
            Dictionary with response text and metadata.
        """
        if provider != "mock":
            raise ValueError(f"MockLLM only supports 'mock' provider, got '{provider}'")
        
        # Create deterministic selection based on prompt hash
        prompt_hash = self._hash_prompt(prompt)
        category = self._select_category(prompt)
        templates = self.RESPONSE_TEMPLATES[category]
        
        # Select template deterministically based on hash
        template_idx = prompt_hash % len(templates)
        response_text = templates[template_idx]
        
        # Add some deterministic variation based on hash
        variation = (prompt_hash % 10) / 10.0  # 0.0 to 0.9
        if variation > 0.7:
            response_text += " [additional context]"
        elif variation > 0.4:
            response_text += " [clarification needed]"
        
        return {
            "text": response_text,
            "provider": "mock",
            "model": "mock-model-v1",
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(prompt.split()) + len(response_text.split()),
            },
            "seed": self.seed,
            "category": category,
        }
    
    def set_seed(self, seed: int) -> None:
        """Update the seed for subsequent calls.
        
        Args:
            seed: New random seed.
        """
        self.seed = seed
        self._rng = random.Random(seed)


# Global instance for convenience
_default_mock_llm = MockLLM(seed=42)


def get_mock_llm(seed: int = 42) -> MockLLM:
    """Get a MockLLM instance with specified seed.
    
    Args:
        seed: Random seed for the instance.
        
    Returns:
        MockLLM instance.
    """
    return MockLLM(seed=seed)
