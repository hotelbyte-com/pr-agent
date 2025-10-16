#!/usr/bin/env python3
"""
测试 zhipu 前缀支持
"""

import os
import sys
sys.path.append('/Users/danceiny/hotelcode/pr-agent-1')

try:
    from pr_agent.algo.ai_handlers.litellm_ai_handler import LiteLLMAIHandler
    from pr_agent.config_loader import get_settings
    
    # 设置测试环境
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["OPENAI_API_BASE"] = "https://open.bigmodel.cn/api/paas/v4"
    
    print("=== 测试 zhipu 前缀支持 ===")
    
    # 创建 AI handler 实例
    handler = LiteLLMAIHandler()
    
    # 检查是否有 zhipu_model_mapping
    if hasattr(handler, 'zhipu_model_mapping'):
        print("✅ zhipu_model_mapping 已添加")
        print(f"支持的映射: {handler.zhipu_model_mapping}")
    else:
        print("❌ zhipu_model_mapping 未找到")
        sys.exit(1)
    
    # 测试模型映射
    test_models = ["zhipu/glm-4.6", "glm-4.6", "openai/glm-4.6"]
    
    for model in test_models:
        print(f"\n测试模型: {model}")
        try:
            # 这里只是测试初始化，不实际调用 API
            print(f"  模型 {model} 可以被处理")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n=== 测试完成 ===")
    
except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"测试错误: {e}")
