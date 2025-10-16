# Zhipu GLM 模型配置指南

## 1. 环境变量配置

```bash
export OPENAI_KEY="your-zhipu-api-key"
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
