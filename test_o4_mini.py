import os
import litellm
from pr_agent.config_loader import get_settings

# 设置测试环境
os.environ['OPENAI_KEY'] = 'test-key'  # 使用测试密钥

# 初始化 litellm
litellm.api_key = "test-key"

print("Testing o4-mini model configuration...")
print(f"litellm version: {litellm.__version__}")

# 检查模型是否在 litellm 的模型列表中
try:
    from litellm import model_cost
    if 'o4-mini' in model_cost:
        print("✓ o4-mini found in litellm model_cost")
        print(f"Model info: {model_cost['o4-mini']}")
    else:
        print("✗ o4-mini NOT found in litellm model_cost")
        print("Available OpenAI models:")
        for model in model_cost:
            if 'gpt' in model or 'o1' in model or 'o4' in model:
                print(f"  - {model}")
except Exception as e:
    print(f"Error checking model_cost: {e}")

# 尝试验证模型
try:
    response = litellm.validate_environment('o4-mini')
    print(f"✓ Model validation passed: {response}")
except Exception as e:
    print(f"✗ Model validation failed: {e}")

# 检查 pr-agent 配置
try:
    from pr_agent.algo import MAX_TOKENS
    if 'o4-mini' in MAX_TOKENS:
        print(f"✓ o4-mini found in pr-agent MAX_TOKENS: {MAX_TOKENS['o4-mini']}")
    else:
        print("✗ o4-mini NOT found in pr-agent MAX_TOKENS")
except Exception as e:
    print(f"Error checking pr-agent config: {e}")
