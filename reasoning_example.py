from openai import OpenAI
from typing import List, Dict, Any
import json

client = OpenAI()

def demonstrate_cot_reasoning(problem: str = None) -> Dict[str, Any]:
    """
    演示链式思维(Chain of Thought)推理
    通过引导模型一步步思考来解决复杂问题
    """
    if problem is None:
        problem = "小明买了3个苹果，每个苹果5元。小红买了2个梨，每个梨4元。他们一共花了多少钱？"

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 使用GPT-4以获得更好的推理能力
            messages=[
                {"role": "system", "content": """你是一个专业的数学解题助手。
解题时请遵循以下步骤：
1. 分析问题中的已知条件
2. 列出解题步骤
3. 逐步计算
4. 得出最终结果
请在每个步骤前标明步骤编号。"""},
                {"role": "user", "content": problem}
            ],
            temperature=0.2,  # 降低随机性，保持逻辑性
            max_tokens=500,
            top_p=0.9,
        )
        return {
            "success": True,
            "reasoning": response.choices[0].message.content
        }

def solve_complex_task(task: str = None) -> Dict[str, Any]:
    """
    演示系统设计推理
    通过分解复杂任务并逐步解决
    """
    if task is None:
        task = """设计一个在线书店系统的主要功能和架构"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """你是一个专业的系统设计专家。
分析问题时请遵循以下框架：
1. 需求分析：列出核心功能需求
2. 系统架构：描述主要组件
3. 数据模型：设计核心数据结构
4. 接口设计：定义关键API
5. 技术选型：推荐适合的技术栈
6. 扩展性考虑：分析可能的扩展点
请在每个部分前标明编号，并详细展开说明。"""},
                {"role": "user", "content": task}
            ],
            temperature=0.3,
            max_tokens=1000,
            top_p=0.9,
        )
        return {
            "success": True,
            "design": response.choices[0].message.content
        }

def demonstrate_step_by_step_coding(problem: str = None) -> Dict[str, Any]:
    """
    演示编程问题的步骤分解和解决
    通过引导模型逐步思考和编写代码
    """
    if problem is None:
        problem = "编写一个函数，找出数组中的第二大的数"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """你是一个专业的编程教练。
解决编程问题时请遵循以下步骤：
1. 问题分析：理解问题要求
2. 思路说明：描述解决方案
3. 代码实现：编写示例代码
4. 复杂度分析：分析时间和空间复杂度
5. 测试用例：提供测试样例
请在每个步骤前标明编号。"""},
                {"role": "user", "content": problem}
            ],
            temperature=0.2,
            max_tokens=800,
            top_p=0.9,
        )
        return {
            "success": True,
            "solution": response.choices[0].message.content
        } 