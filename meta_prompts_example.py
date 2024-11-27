from openai import OpenAI
from typing import Dict, List, Any, Union
import json
import asyncio

class MetaPromptGenerator:
    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        
    async def generate_meta_prompt(
        self,
        task_description: str,
        example_inputs: List[str] = None,
        example_outputs: List[str] = None,
        target_audience: str = None,
        constraints: List[str] = None
    ) -> Dict[str, Any]:
        """
        生成元提示
        
        参数:
        - task_description: 任务描述
        - example_inputs: 示例输入列表
        - example_outputs: 示例输出列表
        - target_audience: 目标受众
        - constraints: 约束条件列表
        """
        try:
            # 构建元提示模板
            meta_prompt = f"""
            作为一个提示工程专家，请帮我为以下任务创建一个最优的提示：

            任务描述：
            {task_description}

            {f'目标受众：{target_audience}' if target_audience else ''}

            {f'约束条件：' + ''.join(f'- {c}' for c in constraints) if constraints else ''}

            {f'示例输入输出：' + ''.join(f'输入: {i}输出: {o}' for i, o in zip(example_inputs, example_outputs)) if example_inputs and example_outputs else ''}

            请生成一个结构化的提示，包含：
            1. 主要指令
            2. 上下文信息
            3. 输入格式要求
            4. 输出格式要求
            5. 示例（如果适用）
            6. 约束和限制
            7. 评估标准

            同时解释为什么这个提示结构是有效的。
            """

            # 生成提示
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的提示工程专家，擅长创建高质量、结构化的提示。"
                    },
                    {
                        "role": "user",
                        "content": meta_prompt
                    }
                ],
                temperature=0.7
            )
            
            return {
                "success": True,
                "prompt": response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def test_generated_prompt(
        self,
        generated_prompt: str,
        test_inputs: List[str]
    ) -> Dict[str, Any]:
        """
        测试生成的提示
        
        参数:
        - generated_prompt: 生成的提示
        - test_inputs: 测试输入列表
        """
        try:
            results = []
            for test_input in test_inputs:
                # 使用生成的提示处理测试输入
                response = await self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {
                            "role": "system",
                            "content": generated_prompt
                        },
                        {
                            "role": "user",
                            "content": test_input
                        }
                    ],
                    temperature=0.7
                )
                
                results.append({
                    "input": test_input,
                    "output": response.choices[0].message.content
                })
            
            return {
                "success": True,
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def refine_prompt(
        self,
        original_prompt: str,
        feedback: str
    ) -> Dict[str, Any]:
        """
        基于反馈优化提示
        
        参数:
        - original_prompt: 原始提示
        - feedback: 优化反馈
        """
        try:
            refinement_prompt = f"""
            请基于以下反馈优化这个提示：

            原始提示：
            {original_prompt}

            反馈：
            {feedback}

            请提供：
            1. 优化后的提示
            2. 改进说明
            3. 预期效果
            """

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的提示优化专家。"
                    },
                    {
                        "role": "user",
                        "content": refinement_prompt
                    }
                ],
                temperature=0.7
            )
            
            return {
                "success": True,
                "refined_prompt": response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

async def demonstrate_meta_prompts():
    """演示元提示生成和优化"""
    generator = MetaPromptGenerator()
    
    try:
        # 示例1：代码审查提示
        print("=== 示例1：代码审查提示生成 ===")
        code_review_task = {
            "task_description": "创建一个代码审查助手，帮助开发者审查Python代码",
            "example_inputs": [
                "def calculate_sum(a, b):    return a + b",
                "class User:    def __init__(self):        pass"
            ],
            "example_outputs": [
                "代码风格良好，但建议添加类型提示和文档字符串。",
                "类定义需要添加属性和方法，当前实现过于简单。"
            ],
            "constraints": [
                "必须检查代码风格",
                "必须检查潜在的bug",
                "必须提供改进建议"
            ]
        }
        
        result = await generator.generate_meta_prompt(**code_review_task)
        if result["success"]:
            print("生成的代码审查提示:")
            print(result["prompt"])
            
            # 测试生成的提示
            test_inputs = [
                """
                def process_data(data):
                    for i in range(len(data)):
                        data[i] = data[i] * 2
                    return data
                """
            ]
            
            test_result = await generator.test_generated_prompt(
                result["prompt"],
                test_inputs
            )
            
            if test_result["success"]:
                print("测试结果:")
                for r in test_result["results"]:
                    print(f"输入:{r['input']}")
                    print(f"输出:{r['output']}")
        
        # 示例2：文章摘要提示
        print("=== 示例2：文章摘要提示生成 ===")
        summarization_task = {
            "task_description": "创建一个文章摘要生成器，能够提取文章的关键信息",
            "target_audience": "内容编辑和研究人员",
            "constraints": [
                "摘要长度不超过200字",
                "保留原文的关键观点",
                "使用客观的语气"
            ]
        }
        
        result = await generator.generate_meta_prompt(**summarization_task)
        if result["success"]:
            print("生成的摘要提示:")
            print(result["prompt"])
            
            # 优化提示
            feedback = """
            1. 需要更明确的结构化输出格式
            2. 添加关键词提取要求
            3. 增加可读性评分标准
            """
            
            refined_result = await generator.refine_prompt(
                result["prompt"],
                feedback
            )
            
            if refined_result["success"]:
                print("优化后的提示:")
                print(refined_result["refined_prompt"])

    except Exception as e:
        print(f"演示过程中出错: {str(e)}")

if __name__ == "__main__":
    asyncio.run(demonstrate_meta_prompts()) 