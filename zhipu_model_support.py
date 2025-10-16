#!/usr/bin/env python3
"""
优雅的 Zhipu GLM 模型支持集成方案

这个模块提供了一个更加优雅和可维护的方式来为 pr-agent 添加 zhipu/ 前缀支持
不需要修改现有代码，而是通过扩展的方式实现
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional

class ZhipuModelMapper:
    """Zhipu 模型映射器"""
    
    def __init__(self):
        self.model_mapping = {
            "zhipu/glm-4.6": "openai/glm-4.6",
            "zhipu/glm-4-plus": "openai/glm-4-plus", 
            "zhipu/glm-4": "openai/glm-4",
            "zhipu/glm-3-turbo": "openai/glm-3-turbo",
        }
    
    def map_model(self, model: str) -> str:
        """
        将 zhipu/ 前缀的模型映射到 openai/ 前缀
        
        Args:
            model: 原始模型名称
            
        Returns:
            映射后的模型名称
        """
        if model in self.model_mapping:
            mapped_model = self.model_mapping[model]
            print(f"🔄 映射模型: {model} -> {mapped_model}")
            return mapped_model
        return model
    
    def is_zhipu_model(self, model: str) -> bool:
        """检查是否为 zhipu 模型"""
        return model.startswith("zhipu/")
    
    def get_supported_models(self) -> Dict[str, str]:
        """获取支持的模型映射"""
        return self.model_mapping.copy()

class ZhipuEnvironmentSetup:
    """Zhipu 环境设置"""
    
    @staticmethod
    def setup_zhipu_environment():
        """设置 Zhipu API 环境变量"""
        if not os.getenv("OPENAI_API_BASE"):
            os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
            print("🔧 设置 OPENAI_API_BASE 为 Zhipu API 端点")
        
        if not os.getenv("OPENAI_KEY"):
            print("⚠️  警告: 未设置 OPENAI_KEY，请确保设置了有效的 Zhipu API Key")
    
    @staticmethod
    def validate_environment() -> bool:
        """验证环境配置"""
        api_key = os.getenv("OPENAI_KEY")
        api_base = os.getenv("OPENAI_API_BASE")
        
        if not api_key:
            print("❌ 缺少 OPENAI_KEY 环境变量")
            return False
        
        if not api_base or "bigmodel.cn" not in api_base:
            print("❌ OPENAI_API_BASE 未设置为 Zhipu API 端点")
            return False
        
        print("✅ Zhipu 环境配置验证通过")
        return True

def patch_pr_agent_for_zhipu():
    """
    为 pr-agent 添加 zhipu 支持的补丁函数
    这是一个非侵入式的方法，通过 monkey patching 实现
    """
    try:
        # 动态导入 pr-agent 模块
        from pr_agent.algo.ai_handlers.litellm_ai_handler import LiteLLMAIHandler
        
        # 创建模型映射器
        mapper = ZhipuModelMapper()
        
        # 保存原始的 chat_completion 方法
        original_chat_completion = LiteLLMAIHandler.chat_completion
        
        def patched_chat_completion(self, model, system, user, **kwargs):
            """带有 zhipu 模型映射的 chat_completion 方法"""
            # 映射 zhipu 模型
            mapped_model = mapper.map_model(model)
            
            # 调用原始方法
            return original_chat_completion(self, mapped_model, system, user, **kwargs)
        
        # 应用补丁
        LiteLLMAIHandler.chat_completion = patched_chat_completion
        
        print("✅ 成功为 pr-agent 添加 zhipu 模型支持 (非侵入式)")
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入 pr-agent 模块: {e}")
        return False
    except Exception as e:
        print(f"❌ 补丁应用失败: {e}")
        return False

def create_configuration_guide():
    """创建配置指南"""
    
    guide_content = """# Zhipu GLM 模型配置指南

## 1. 环境变量配置

```bash
export OPENAI_API_KEY="your-zhipu-api-key"
export OPENAI_API_BASE="https://open.bigmodel.cn/api/paas/v4"
```

## 2. pr-agent 配置文件 (.pr_agent.toml)

```toml
[config]
model = "zhipu/glm-4.6"  # 或者使用 "openai/glm-4.6"
max_model_tokens = 200000

[github_action_config]
model = "zhipu/glm-4.6"
pr_actions = ["opened", "reopened", "ready_for_review", "review_requested", "synchronize"]
```

## 3. GitHub Actions 配置

```yaml
name: PR Agent

on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]
  issue_comment:
    types: [created, edited]

jobs:
  pr_agent_job:
    runs-on: ubuntu-latest
    steps:
      - name: PR Agent action step
        uses: Codium-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.ZHIPU_API_KEY }}
          OPENAI_API_BASE: "https://open.bigmodel.cn/api/paas/v4"
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          github_action_config.model: "zhipu/glm-4.6"
          github_action_config.pr_actions: '["opened", "reopened", "ready_for_review", "review_requested", "synchronize"]'
```

## 4. 支持的模型格式

- `zhipu/glm-4.6` (推荐，会自动映射到 openai/glm-4.6)
- `openai/glm-4.6` (直接使用)
- `glm-4.6` (需要正确的环境变量配置)

## 5. 使用方法

### 方法一：使用补丁脚本 (修改源码)
```bash
python zhipu_provider_patch.py
```

### 方法二：使用非侵入式集成 (推荐)
```python
from zhipu_model_support import patch_pr_agent_for_zhipu, ZhipuEnvironmentSetup

# 设置环境
ZhipuEnvironmentSetup.setup_zhipu_environment()

# 应用补丁
patch_pr_agent_for_zhipu()

# 现在可以使用 zhipu/ 前缀的模型了
```

## 6. 验证配置

```python
from zhipu_model_support import ZhipuEnvironmentSetup

# 验证环境配置
if ZhipuEnvironmentSetup.validate_environment():
    print("✅ 配置正确")
else:
    print("❌ 配置有问题")
```
"""
    
    guide_path = Path.cwd() / "ZHIPU_CONFIGURATION_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ 创建配置指南: {guide_path}")

def main():
    """主函数 - 演示如何使用"""
    print("🚀 Zhipu GLM 模型支持集成")
    print("=" * 50)
    
    # 1. 设置环境
    print("\n1. 设置 Zhipu 环境...")
    ZhipuEnvironmentSetup.setup_zhipu_environment()
    
    # 2. 验证环境
    print("\n2. 验证环境配置...")
    is_valid = ZhipuEnvironmentSetup.validate_environment()
    
    # 3. 应用补丁
    print("\n3. 应用 zhipu 模型支持...")
    patch_success = patch_pr_agent_for_zhipu()
    
    # 4. 显示支持的模型
    print("\n4. 支持的模型映射:")
    mapper = ZhipuModelMapper()
    for original, mapped in mapper.get_supported_models().items():
        print(f"   {original} -> {mapped}")
    
    # 5. 创建配置指南
    print("\n5. 创建配置指南...")
    create_configuration_guide()
    
    print("\n" + "=" * 50)
    print("🎉 集成完成!")
    
    if patch_success and is_valid:
        print("✅ 现在可以在 pr-agent 中使用 zhipu/ 前缀的 GLM 模型了")
    else:
        print("⚠️  请检查环境配置和依赖")
    
    print("\n📖 查看详细配置指南: ZHIPU_CONFIGURATION_GUIDE.md")

if __name__ == "__main__":
    main()