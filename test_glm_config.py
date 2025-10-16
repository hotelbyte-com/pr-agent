import os
import litellm
from pr_agent.config_loader import get_settings

print("Testing GLM model configuration...")

# 检查 litellm 版本
try:
    import pkg_resources
    version = pkg_resources.get_distribution("litellm").version
    print(f"litellm version: {version}")
except:
    print("Could not determine litellm version")

# 检查 GLM 模型在 litellm 中的配置
try:
    from litellm import model_cost
    glm_models = [model for model in model_cost if 'glm' in model.lower()]
    print(f"GLM models found in litellm: {glm_models}")
    
    # 检查具体的 GLM 模型
    test_models = ['glm-4.6', 'zhipu/glm-4.6']
    for model in test_models:
        if model in model_cost:
            print(f"✓ {model} found in model_cost")
            print(f"  Provider: {model_cost[model].get('litellm_provider', 'unknown')}")
        else:
            print(f"✗ {model} NOT found in model_cost")
            
except Exception as e:
    print(f"Error checking model_cost: {e}")

# 检查 pr-agent 配置
try:
    from pr_agent.algo import MAX_TOKENS
    glm_in_max_tokens = [model for model in MAX_TOKENS if 'glm' in model.lower()]
    print(f"GLM models in pr-agent MAX_TOKENS: {glm_in_max_tokens}")
    
    for model in ['glm-4.6', 'zhipu/glm-4.6']:
        if model in MAX_TOKENS:
            print(f"✓ {model} found in MAX_TOKENS: {MAX_TOKENS[model]}")
        else:
            print(f"✗ {model} NOT found in MAX_TOKENS")
            
except Exception as e:
    print(f"Error checking pr-agent config: {e}")

# 测试模型验证
print("\nTesting model validation...")
test_models = ['glm-4.6', 'zhipu/glm-4.6']
for model in test_models:
    try:
        # 尝试验证模型
        response = litellm.validate_environment(model)
        print(f"✓ {model} validation passed")
    except Exception as e:
        print(f"✗ {model} validation failed: {e}")
