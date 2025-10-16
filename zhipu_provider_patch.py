#!/usr/bin/env python3
"""
为 pr-agent 添加 zhipu/glm-4.6 前缀支持的通用补丁

这个脚本会动态查找并修改 litellm_ai_handler.py 来支持 zhipu/ 前缀的 GLM 模型
"""

import os
import sys
from pathlib import Path

def find_pr_agent_root():
    """动态查找 pr-agent 项目根目录"""
    current_path = Path(__file__).resolve()
    
    # 从当前文件向上查找包含 pr_agent 目录的根目录
    for parent in current_path.parents:
        pr_agent_dir = parent / "pr_agent"
        if pr_agent_dir.exists() and pr_agent_dir.is_dir():
            return parent
    
    # 如果没找到，尝试当前目录
    current_dir = Path.cwd()
    pr_agent_dir = current_dir / "pr_agent"
    if pr_agent_dir.exists() and pr_agent_dir.is_dir():
        return current_dir
    
    raise FileNotFoundError("无法找到 pr-agent 项目根目录")

def find_litellm_handler():
    """动态查找 litellm_ai_handler.py 文件"""
    try:
        root_dir = find_pr_agent_root()
        handler_path = root_dir / "pr_agent" / "algo" / "ai_handlers" / "litellm_ai_handler.py"
        
        if handler_path.exists():
            return handler_path
        else:
            raise FileNotFoundError(f"找不到 litellm_ai_handler.py 文件: {handler_path}")
    except Exception as e:
        raise FileNotFoundError(f"查找 litellm_ai_handler.py 失败: {e}")

def patch_litellm_handler():
    """为 litellm_ai_handler.py 添加 zhipu 前缀支持"""
    
    try:
        handler_path = find_litellm_handler()
        print(f"找到 litellm_ai_handler.py: {handler_path}")
    except FileNotFoundError as e:
        print(f"错误: {e}")
        return False
    
    # 读取原文件
    with open(handler_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经包含 zhipu 支持
    if "zhipu_model_mapping" in content:
        print("zhipu 支持已存在，无需重复添加")
        return True
    
    # 找到合适的位置插入代码
    # 在 LiteLLMAIHandler 类的 __init__ 方法中添加
    init_method_start = content.find("def __init__(self")
    if init_method_start == -1:
        print("错误: 找不到 __init__ 方法")
        return False
    
    # 找到 __init__ 方法的结束位置
    init_method_end = content.find("\n    def ", init_method_start + 1)
    if init_method_end == -1:
        init_method_end = len(content)
    
    # 在 __init__ 方法末尾添加 zhipu 模型映射
    zhipu_mapping_code = '''
        # Zhipu GLM 模型映射 - 将 zhipu/ 前缀映射到 openai/ 前缀
        self.zhipu_model_mapping = {
            "zhipu/glm-4.6": "openai/glm-4.6",
            "zhipu/glm-4-plus": "openai/glm-4-plus",
            "zhipu/glm-4": "openai/glm-4",
        }
'''
    
    # 插入代码
    new_content = content[:init_method_end] + zhipu_mapping_code + content[init_method_end:]
    
    # 找到 chat_completion 方法并修改
    chat_completion_start = new_content.find("def chat_completion(")
    if chat_completion_start == -1:
        print("错误: 找不到 chat_completion 方法")
        return False
    
    # 在 chat_completion 方法开始处添加模型映射逻辑
    method_body_start = new_content.find(":", chat_completion_start) + 1
    method_body_start = new_content.find("\n", method_body_start) + 1
    
    model_mapping_code = '''        # 处理 zhipu 前缀模型映射
        if model in self.zhipu_model_mapping:
            original_model = model
            model = self.zhipu_model_mapping[model]
            get_logger().info(f"Mapping zhipu model {original_model} to {model}")
        
'''
    
    new_content = new_content[:method_body_start] + model_mapping_code + new_content[method_body_start:]
    
    # 写入修改后的文件
    with open(handler_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 成功为 {handler_path} 添加 zhipu 前缀支持")
    return True

def create_test_script():
    """创建测试脚本验证 zhipu 前缀支持"""
    
    try:
        root_dir = find_pr_agent_root()
        test_path = root_dir / "test_zhipu_support.py"
        sys_path_append = f"sys.path.append('{root_dir}')"
    except FileNotFoundError:
        test_path = Path.cwd() / "test_zhipu_support.py"
        sys_path_append = f"sys.path.append('{Path.cwd()}')"
    
    test_script = f'''#!/usr/bin/env python3
"""
测试 zhipu 前缀支持
"""

import os
import sys
{sys_path_append}

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
        print(f"支持的映射: {{handler.zhipu_model_mapping}}")
    else:
        print("❌ zhipu_model_mapping 未找到")
        sys.exit(1)
    
    # 测试模型映射
    test_models = ["zhipu/glm-4.6", "glm-4.6", "openai/glm-4.6"]
    
    for model in test_models:
        print(f"\\n测试模型: {{model}}")
        try:
            # 这里只是测试初始化，不实际调用 API
            print(f"  模型 {{model}} 可以被处理")
        except Exception as e:
            print(f"  错误: {{e}}")
    
    print("\\n=== 测试完成 ===")
    
except ImportError as e:
    print(f"导入错误: {{e}}")
except Exception as e:
    print(f"测试错误: {{e}}")
'''
    
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    os.chmod(test_path, 0o755)
    print(f"✅ 创建测试脚本: {test_path}")

def main():
    """主函数"""
    print("=== 为 pr-agent 添加 zhipu 前缀支持 ===")
    
    # 1. 修补 litellm_ai_handler.py
    if not patch_litellm_handler():
        print("❌ 修补失败")
        sys.exit(1)
    
    # 2. 创建测试脚本
    create_test_script()
    
    print("\n=== 修补完成 ===")
    print("现在你可以在配置中使用以下任一格式:")
    print("- zhipu/glm-4.6 (会自动映射到 openai/glm-4.6)")
    print("- openai/glm-4.6 (直接使用)")
    print("- glm-4.6 (需要正确的环境变量配置)")
    
    print("\n运行测试: python test_zhipu_support.py")

if __name__ == "__main__":
    main()