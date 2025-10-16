import pytest
from pr_agent.algo import MAX_TOKENS
from pr_agent.algo.utils import get_max_tokens
import pr_agent.algo.utils as utils


class TestGLMModelSupport:
    """Test GLM-4.6 model support in PR Agent."""

    def test_glm_model_in_max_tokens(self):
        """Test that GLM models are included in MAX_TOKENS dictionary."""
        assert "glm-4.6" in MAX_TOKENS
        assert "zhipu/glm-4.6" in MAX_TOKENS
        assert MAX_TOKENS["glm-4.6"] == 200000
        assert MAX_TOKENS["zhipu/glm-4.6"] == 200000

    def test_get_max_tokens_for_glm(self, monkeypatch):
        """Test get_max_tokens function with GLM models."""
        # Mock the configuration
        monkeypatch.setattr(utils.get_settings(), "config", type('obj', (object,), {
            'model': 'glm-4.6',
            'max_model_tokens': None
        })())
        
        max_tokens = get_max_tokens('glm-4.6')
        assert max_tokens == 200000, f"Expected 200000 tokens for glm-4.6, got {max_tokens}"

        # Test with zhipu prefix
        monkeypatch.setattr(utils.get_settings(), "config", type('obj', (object,), {
            'model': 'zhipu/glm-4.6',
            'max_model_tokens': None
        })())
        
        max_tokens = get_max_tokens('zhipu/glm-4.6')
        assert max_tokens == 200000

    def test_get_max_tokens_with_limit_for_glm(self, monkeypatch):
        """Test get_max_tokens function with GLM models and custom limit."""
        # Mock the configuration with custom limit
        monkeypatch.setattr(utils.get_settings(), "config", type('obj', (object,), {
            'model': 'glm-4.6',
            'max_model_tokens': 100000
        })())
        
        max_tokens = get_max_tokens('glm-4.6')
        assert max_tokens == 100000, f"Expected 100000 tokens (limited), got {max_tokens}"