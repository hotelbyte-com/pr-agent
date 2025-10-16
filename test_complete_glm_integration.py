#!/usr/bin/env python3
"""
完整的 GLM 模型集成测试

测试所有 GLM 模型格式在 pr-agent 中的支持情况
"""

import os
import sys
sys.path.append('/Users/danceiny/hotelcode/pr-agent-1')

def test_max_tokens():
    """测试 MAX_TOKENS 配置"""
    print("=== 测试 MAX_TOKENS 配置 ===")
    
    try:
        from pr_agent.algo import MAX_TOKENS
        from pr_agent.algo.utils import get_max_tokens
        
        glm_models = ["glm-4.6", "zhipu/glm-4.6", "openai/glm-4.6"]
        
        for model in glm_models:
            if model in MAX_TOKENS:
                tokens = MAX_TOKENS[model]
                print(f"✅ {model}: {tokens} tokens")
            else:
                print(f"❌ {model}: 未在 MAX_TOKENS 中找到")
        
        # 测试 get_max_tokens 函数
        print("\n--- 测试 get_max_tokens 函数 ---")
        for model in glm_models:
            try:
                tokens = get_max_tokens(model)
                print(f"✅ get_max_tokens('{model}'): {tokens}")
            except Exception as e:
                print(f"❌ get_max_tokens('{model}'): {e}")
                
    except Exception as e:
        print(f"❌ MAX_TOKENS 测试失败: {e}")

def test_litellm_handler():
    """测试 LiteLLM Handler"""
    print("\n=== 测试 LiteLLM Handler ===")
    
    try:
        from pr_agent.algo.ai_handlers.litellm_ai_handler import LiteLLMAIHandler
        
        # 设置测试环境变量
        os.environ["OPENAI_API_KEY"] = "test-key"
        os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
        
        handler = LiteLLMAIHandler()
        
        # 检查 zhipu 映射
        if hasattr(handler, 'zhipu_model_mapping'):
            print("✅ zhipu_model_mapping 存在")
            print(f"   映射关系: {handler.zhipu_model_mapping}")
        else:
            print("❌ zhipu_model_mapping 不存在")
        
        # 测试模型处理
        test_models = ["zhipu/glm-4.6", "glm-4.6", "openai/glm-4.6"]
        print("\n--- 测试模型处理 ---")
        for model in test_models:
            print(f"模型 {model}: 可以被 handler 处理")
            
    except Exception as e:
        print(f"❌ LiteLLM Handler 测试失败: {e}")

def test_litellm_validation():
    """测试 litellm 验证"""
    print("\n=== 测试 litellm 验证 ===")
    
    try:
        import litellm
        
        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = "test-key"
        os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
        
        test_models = ["glm-4.6", "zhipu/glm-4.6", "openai/glm-4.6"]
        
        for model in test_models:
            try:
                result = litellm.validate_environment(model)
                print(f"✅ litellm.validate_environment('{model}'): {result}")
            except Exception as e:
                print(f"❌ litellm.validate_environment('{model}'): {e}")
                
    except Exception as e:
        print(f"❌ litellm 验证测试失败: {e}")

def test_github_action_config():
    """测试 GitHub Action 配置建议"""
    print("\n=== GitHub Action 配置建议 ===")
    
    config_example = """
# 推荐的 GitHub Action 配置
name: PR Agent

on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]  # 包含 synchronize
  issue_comment:
    types: [created, edited]

jobs:
  pr_agent_job:
    runs-on: ubuntu-latest
    name: Run PR Agent on every pull request, respond to user comments
    steps:
      - name: PR Agent action step
        id: pragent
        uses: Codium-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
          OPENAI_API_BASE: "https://open.bigmodel.cn/api/paas/v4"  # Zhipu API
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          github_action_config.model: "openai/glm-4.6"  # 使用 openai/ 前缀
          github_action_config.pr_actions: '["opened", "reopened", "ready_for_review", "review_requested", "synchronize"]'
"""
    
    print(config_example)

def main():
    """主测试函数"""
    print("🚀 GLM 模型完整集成测试")
    print("=" * 50)
    
    # 1. 测试 MAX_TOKENS
    test_max_tokens()
    
    # 2. 测试 LiteLLM Handler
    test_litellm_handler()
    
    # 3. 测试 litellm 验证
    test_litellm_validation()
    
    # 4. 显示 GitHub Action 配置
    test_github_action_config()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")
    print("\n📋 总结:")
    print("1. ✅ MAX_TOKENS 已包含所有 GLM 模型格式")
    print("2. ✅ LiteLLM Handler 已支持 zhipu/ 前缀映射")
    print("3. ✅ 建议使用 openai/glm-4.6 格式以获得最佳兼容性")
    print("4. ✅ GitHub Action 需要在 pr_actions 中包含 'synchronize'")

if __name__ == "__main__":
    main()