#!/usr/bin/env python3
"""
测试 GLM 模型的实际调用
"""

import os
import sys
sys.path.append('/Users/danceiny/hotelcode/pr-agent-1')

try:
    import litellm
    
    # 设置测试环境变量
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
    
    print(f"litellm version: {litellm.__version__ if hasattr(litellm, '__version__') else 'unknown'}")
    
    # 测试不同的模型名称格式
    test_models = [
        "glm-4.6",
        "zhipu/glm-4.6",
        "openai/glm-4.6"
    ]
    
    messages = [{"role": "user", "content": "Hello"}]
    
    for model in test_models:
        print(f"\nTesting model: {model}")
        try:
            # 尝试创建 completion（不实际发送请求）
            response = litellm.completion(
                model=model,
                messages=messages,
                mock_response="This is a test response",  # 使用 mock 响应避免实际 API 调用
                api_base=os.environ.get("OPENAI_API_BASE"),
                api_key=os.environ.get("OPENAI_API_KEY")
            )
            print(f"  Success: {response}")
        except Exception as e:
            print(f"  Error: {e}")
            
            # 尝试获取更详细的错误信息
            if "LLM Provider NOT provided" in str(e):
                print(f"  -> Provider not recognized for model: {model}")
                print(f"  -> Suggestion: Try using 'openai/glm-4.6' format")
            elif "BadRequestError" in str(e):
                print(f"  -> API request error (expected with test key)")
            else:
                print(f"  -> Other error: {type(e).__name__}")

    # 检查 litellm 如何解析模型名称
    print(f"\nChecking model name parsing:")
    
    for model in test_models:
        try:
            from litellm.litellm_core_utils.get_llm_provider_logic import get_llm_provider
            provider, model_name, dynamic_api_key, api_base = get_llm_provider(
                model=model,
                custom_llm_provider=None,
                api_base=None,
                api_version=None
            )
            print(f"  {model} -> provider: {provider}, model_name: {model_name}")
        except Exception as e:
            print(f"  {model} -> parsing error: {e}")

except ImportError as e:
    print(f"Could not import litellm: {e}")
except Exception as e:
    print(f"Error: {e}")