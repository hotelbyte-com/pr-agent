#!/usr/bin/env python3
"""
测试 litellm 对 zhipu 模型的原生支持
验证是否真的需要前缀映射
"""

import os
import litellm

def test_zhipu_native_support():
    """测试 litellm 对 zhipu 模型的原生支持"""
    print("=== 测试 litellm 对 zhipu 模型的原生支持 ===\n")
    
    # 设置环境变量
    os.environ["OPENAI_KEY"] = "test-key"
    os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
    
    # 测试不同的模型格式
    test_models = [
        "glm-4.6",
        "zhipu/glm-4.6", 
        "openai/glm-4.6"
    ]
    
    print("1. 检查 litellm 支持的 providers:")
    try:
        providers = litellm.provider_list
        print(f"   支持的 providers: {len(providers)} 个")
        zhipu_providers = [p for p in providers if 'zhipu' in p.lower() or 'glm' in p.lower()]
        if zhipu_providers:
            print(f"   Zhipu/GLM 相关 providers: {zhipu_providers}")
        else:
            print("   未找到 Zhipu/GLM 相关 providers")
    except Exception as e:
        print(f"   获取 provider 列表失败: {e}")
    
    print("\n2. 检查模型成本配置:")
    try:
        model_cost = litellm.model_cost
        glm_models = {k: v for k, v in model_cost.items() if 'glm' in k.lower()}
        if glm_models:
            print("   GLM 模型成本配置:")
            for model, cost in glm_models.items():
                print(f"     {model}: {cost}")
        else:
            print("   未找到 GLM 模型成本配置")
    except Exception as e:
        print(f"   获取模型成本配置失败: {e}")
    
    print("\n3. 测试环境验证:")
    for model in test_models:
        try:
            result = litellm.validate_environment(model)
            print(f"   {model}: ✅ {result}")
        except Exception as e:
            print(f"   {model}: ❌ {e}")
    
    print("\n4. 测试模型调用 (不实际发送请求):")
    for model in test_models:
        try:
            # 只测试模型名称解析，不实际调用
            from litellm.utils import get_llm_provider
            provider, model_name, _, _ = get_llm_provider(model)
            print(f"   {model} -> provider: {provider}, model_name: {model_name}")
        except Exception as e:
            print(f"   {model}: ❌ 解析失败: {e}")

def check_pr_agent_max_tokens():
    """检查 pr-agent 的 MAX_TOKENS 配置"""
    print("\n=== 检查 pr-agent MAX_TOKENS 配置 ===")
    
    try:
        from pr_agent.algo import MAX_TOKENS
        
        glm_models = {k: v for k, v in MAX_TOKENS.items() if 'glm' in k.lower()}
        if glm_models:
            print("pr-agent 中的 GLM 模型配置:")
            for model, tokens in glm_models.items():
                print(f"  {model}: {tokens}")
        else:
            print("pr-agent 中未找到 GLM 模型配置")
            
    except Exception as e:
        print(f"检查 pr-agent MAX_TOKENS 失败: {e}")

if __name__ == "__main__":
    test_zhipu_native_support()
    check_pr_agent_max_tokens()
    
    print("\n=== 结论 ===")
    print("如果 litellm 原生支持 zhipu/glm-4.6，那么前缀映射就是不必要的")
    print("如果不支持，我们需要了解具体的错误原因")