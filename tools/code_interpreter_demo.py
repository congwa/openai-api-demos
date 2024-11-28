from openai import OpenAI
import time
from typing import List, Dict, Any
import json

class CodeInterpreterDemo:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
            timeout=300.0  # 默认超时时间
        )
        
    def create_assistant(self) -> str:
        """创建一个具有代码解释器功能的助手"""
        assistant = self.client.beta.assistants.create(
            name="数据分析助手",
            instructions="""你是一个专业的数据分析师和Python程序员。
            你可以帮助用户处理数据分析任务，创建可视化图表，并解决编程问题。
            请用中文回复，并确保代码注释也使用中文。""",
            model="gpt-4-turbo-preview",
            tools=[{"type": "code_interpreter"}]
        )
        return assistant.id

    def create_thread(self) -> str:
        """创建新的对话线程"""
        thread = self.client.beta.threads.create()
        return thread.id

    def add_message(self, thread_id: str, content: str) -> None:
        """向线程添加新消息"""
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )

    def run_assistant(self, thread_id: str, assistant_id: str) -> Dict[str, Any]:
        """运行助手并等待完成"""
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        # 等待运行完成
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            time.sleep(1)
            
        # 获取最新消息
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content

def demo_code_interpreter():
    """演示代码解释器的主要功能"""
    demo = CodeInterpreterDemo()
    
    # 创建助手
    assistant_id = demo.create_assistant()
    print("✅ 助手创建成功")
    
    # 创建对话线程
    thread_id = demo.create_thread()
    print("✅ 对话线程创建成功")
    
    # 示例1：基础数据分析
    data_analysis_prompt = """
    请帮我创建一个示例数据集，包含100行销售数据，
    字段包括：日期、产品类别、销售额、数量。
    然后进行以下分析：
    1. 计算基本统计信息
    2. 创建一个销售趋势图
    3. 按产品类别统计销售情况
    请用图表展示结果。
    """
    
    print("\n🔄 正在处理数据分析请求...")
    demo.add_message(thread_id, data_analysis_prompt)
    response = demo.run_assistant(thread_id, assistant_id)
    print("📊 数据分析结果：")
    print(response)
    
    # 示例2：数学计算和可视化
    math_visualization_prompt = """
    请帮我：
    1. 生成一个正弦波和余弦波的图表
    2. 在同一个图表中显示
    3. 添加图例和标题
    4. 使用不同的颜色区分
    """
    
    print("\n🔄 正在处理数学可视化请求...")
    demo.add_message(thread_id, math_visualization_prompt)
    response = demo.run_assistant(thread_id, assistant_id)
    print("📈 数学可视化结果：")
    print(response)
    
    return {
        "assistant_id": assistant_id,
        "thread_id": thread_id
    }
