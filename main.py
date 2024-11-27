import os
import argparse
import asyncio
# 使用示例
if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='OpenAI API 功能演示')
    parser.add_argument('--api-key', type=str, help='OpenAI API密钥')
    args = parser.parse_args()
    
    # 设置环境变量
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key
    
    # 创建必要的文件和目录
    def setup_environment():
        """设置运行环境"""
        # 创建示例语音文件（如果需要测试语音功能）
        if not os.path.exists("speech.mp3"):
            print("请准备speech.mp3文件用于语音转文字测试")
        
        # 创建示例图片（如果需要测试图片变体功能）
        if not os.path.exists("panda.png"):
            print("请准备panda.png文件用于图片变体测试")
        
        if not os.path.exists("panda1.png"):
            print("请准备panda1.png文件用于图片变体测试")

        if not os.path.exists("panda2.png"):
            print("请准备panda2.png文件用于图片变体测试")
        
        # 创建输出目录
        os.makedirs("output", exist_ok=True)

    # 设置环境
    setup_environment()
    from run import demo_all_features
    
    # 运行演示
    asyncio.run(demo_all_features()) 