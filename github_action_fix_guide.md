# GitHub Action 配置修复指南

## 问题分析

你遇到的 "Skipping action: synchronize" 问题是因为：

1. 你的 GitHub Action 触发器配置了 `synchronize` 事件：
```yaml
on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]
```

2. 但是 pr-agent 的默认 `pr_actions` 配置不包含 `synchronize`：
```python
pr_actions = get_settings().get("GITHUB_ACTION_CONFIG.PR_ACTIONS", 
    ["opened", "reopened", "ready_for_review", "review_requested"])
```

## 解决方案

在你的 GitHub Action 配置中添加 `github_action_config.pr_actions` 环境变量：

```yaml
name: PR Agent
on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]
  issue_comment:
jobs:
  pr_agent_job:
    if: ${{ github.event.sender.type != 'Bot' }}
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: write
    steps:
      - name: PR Agent action step
        uses: qodo-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
          OPENAI_API_BASE: "https://open.bigmodel.cn/api/paas/v4"
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          config.model: "openai/glm-4.6"
          config.fallback_models: '["openai/glm-4.6"]'
          # 关键配置：包含 synchronize 事件
          github_action_config.pr_actions: '["opened", "reopened", "ready_for_review", "synchronize"]'
          github_action_config.auto_review: "true"
          github_action_config.auto_describe: "true"
          github_action_config.auto_improve: "true"
```

## GLM 模型配置

同时修复 GLM 模型配置：

1. 使用 `openai/glm-4.6` 而不是 `zhipu/glm-4.6`
2. 设置正确的 API base URL
3. 确保 API key 正确设置

## 完整的工作配置示例

```yaml
name: PR Agent with GLM
on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]
  issue_comment:
jobs:
  pr_agent_job:
    if: ${{ github.event.sender.type != 'Bot' }}
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: write
    steps:
      - name: PR Agent action step
        uses: qodo-ai/pr-agent@main
        env:
          # GLM API 配置
          OPENAI_KEY: ${{ secrets.GLM_API_KEY }}
          OPENAI_API_BASE: "https://open.bigmodel.cn/api/paas/v4"
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          
          # 模型配置
          config.model: "openai/glm-4.6"
          config.fallback_models: '["openai/glm-4.6"]'
          
          # 事件配置 - 包含 synchronize
          github_action_config.pr_actions: '["opened", "reopened", "ready_for_review", "synchronize"]'
          
          # 工具配置
          github_action_config.auto_review: "true"
          github_action_config.auto_describe: "true"
          github_action_config.auto_improve: "true"
```

## 验证配置

配置完成后，当你推送新的提交到 PR 时，应该会看到：
- 不再有 "Skipping action: synchronize" 消息
- pr-agent 会正常运行并使用 GLM 模型进行分析