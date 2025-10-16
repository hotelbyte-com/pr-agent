#!/usr/bin/env python3
"""
测试 zhipu provider 在 litellm 中的支持情况
"""

import os
import sys
sys.path.append('/Users/danceiny/hotelcode/pr-agent-1')

try:
    import litellm
    print(f"litellm version: {litellm.__version__ if hasattr(litellm, '__version__') else 'unknown'}")
    
    # 检查 zhipu 是否在支持的 providers 中
    if hasattr(litellm, 'provider_list'):
        print(f"Supported providers: {litellm.provider_list}")
    
    # 检查 model_cost 中的 zhipu 模型
    zhipu_models = []
    if hasattr(litellm, 'model_cost'):
        for model_name, model_info in litellm.model_cost.items():
            if 'zhipu' in model_name.lower() or 'glm' in model_name.lower():
                zhipu_models.append((model_name, model_info.get('litellm_provider', 'unknown')))
    
    print(f"\nZhipu/GLM models found in model_cost:")
    for model_name, provider in zhipu_models:
        print(f"  {model_name}: provider={provider}")
    
    # 检查 pr-agent 的 MAX_TOKENS 配置
    try:
        from pr_agent.algo import MAX_TOKENS
        glm_in_max_tokens = []
        for model_name in MAX_TOKENS:
            if 'glm' in model_name.lower() or 'zhipu' in model_name.lower():
                glm_in_max_tokens.append((model_name, MAX_TOKENS[model_name]))
        
        print(f"\nGLM models in pr-agent MAX_TOKENS:")
        for model_name, max_tokens in glm_in_max_tokens:
            print(f"  {model_name}: {max_tokens}")
    except ImportError as e:
        print(f"Could not import pr-agent MAX_TOKENS: {e}")
    
    # 测试 zhipu provider 验证
    print(f"\nTesting zhipu provider validation:")
    
    # 测试不同的模型名称格式
    test_models = [
        "glm-4.6",
        "zhipu/glm-4.6", 
        "glm-4-plus",
        "zhipu/glm-4-plus"
    ]
    
    for model in test_models:
        try:
            # 尝试验证环境
            result = litellm.validate_environment(model=model)
            print(f"  {model}: validation passed - {result}")
        except Exception as e:
            print(f"  {model}: validation failed - {e}")
    
    # 检查是否有 zhipu 相关的配置
    print(f"\nChecking for zhipu configuration in litellm:")
    
    # 检查 litellm 的内部模块
    try:
        import litellm.llms
        print(f"Available LLM modules: {dir(litellm.llms)}")
    except Exception as e:
        print(f"Could not access litellm.llms: {e}")

except ImportError as e:
    print(f"Could not import litellm: {e}")
except Exception as e:
    print(f"Error: {e}")