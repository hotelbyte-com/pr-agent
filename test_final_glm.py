#!/usr/bin/env python3
"""
最终测试 GLM 模型配置修复
"""

import os
import sys
sys.path.append('/Users/danceiny/hotelcode/pr-agent-1')

try:
    import litellm
    
    # 模拟 GitHub Action 中的环境变量设置
    os.environ["OPENAI_API_KEY"] = "9fcd4114657045f693f3e1d0b88fa3da.7A85nV6VHjnv3r85"
    os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
    
    print("=== GLM 模型配置修复测试 ===")
    print(f"litellm version: {litellm.__version__ if hasattr(litellm, '__version__') else 'unknown'}")
    
    # 测试修复后的模型名称格式
    correct_model = "openai/glm-4.6"
    incorrect_models = ["glm-4.6", "zhipu/glm-4.6"]
    
    messages = [{"role": "user", "content": "Hello, this is a test message."}]
    
    print(f"\n1. 测试正确的模型格式: {correct_model}")
    try:
        # 使用 mock 响应测试
        response = litellm.completion(
            model=correct_model,
            messages=messages,
            mock_response="Test response from GLM-4.6",
            api_base=os.environ.get("OPENAI_API_BASE"),
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        print(f"  ✅ 成功: {correct_model} 可以正常工作")
        print(f"  响应: {response.choices[0].message.content}")
    except Exception as e:
        print(f"  ❌ 失败: {e}")
    
    print(f"\n2. 验证错误的模型格式会失败:")
    for model in incorrect_models:
        try:
            response = litellm.completion(
                model=model,
                messages=messages,
                mock_response="This should fail",
                api_base=os.environ.get("OPENAI_API_BASE"),
                api_key=os.environ.get("OPENAI_API_KEY")
            )
            print(f"  ⚠️  意外成功: {model}")
        except Exception as e:
            if "LLM Provider NOT provided" in str(e):
                print(f"  ✅ 预期失败: {model} - Provider 未识别")
            else:
                print(f"  ❌ 其他错误: {model} - {e}")
    
    # 检查 pr-agent 的 MAX_TOKENS 配置
    print(f"\n3. 检查 pr-agent MAX_TOKENS 配置:")
    try:
        from pr_agent.algo import MAX_TOKENS
        
        models_to_check = ["glm-4.6", "zhipu/glm-4.6", "openai/glm-4.6"]
        for model in models_to_check:
            if model in MAX_TOKENS:
                print(f"  ✅ {model}: {MAX_TOKENS[model]} tokens")
            else:
                print(f"  ❌ {model}: 未在 MAX_TOKENS 中找到")
                
        # 建议添加 openai/glm-4.6 到 MAX_TOKENS
        if "openai/glm-4.6" not in MAX_TOKENS:
            print(f"\n  💡 建议: 需要在 MAX_TOKENS 中添加 'openai/glm-4.6': 200000")
        
    except ImportError as e:
        print(f"  ❌ 无法导入 pr-agent MAX_TOKENS: {e}")
    
    print(f"\n=== 修复建议 ===")
    print(f"1. 在 GitHub Action 配置中使用: config.model: \"openai/glm-4.6\"")
    print(f"2. 确保 OPENAI_API_KEY 和 OPENAI_API_BASE 正确设置")
    print(f"3. 如果需要，在 pr_agent/algo/__init__.py 的 MAX_TOKENS 中添加:")
    print(f"   \"openai/glm-4.6\": 200000")

except ImportError as e:
    print(f"Could not import litellm: {e}")
except Exception as e:
    print(f"Error: {e}")