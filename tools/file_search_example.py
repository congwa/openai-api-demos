from openai import OpenAI
import asyncio
import json
import os
from typing import Dict, List, Any
import time

class FileSearchAssistant:
    def __init__(self, client: OpenAI = None):
        """
        初始化文件搜索助手
        
        参数:
        - client: OpenAI客户端实例
        """
        self.client = client or OpenAI()
        self.assistant = None
        self.thread = None
        self.uploaded_files = []
        
    async def setup_assistant(self) -> Dict[str, Any]:
        """
        创建并设置助手
        """
        try:
            # 创建助手
            self.assistant = await self.client.beta.assistants.create(
                name="文件搜索助手",
                description="一个专门用于文件搜索和分析的助手",
                model="gpt-4-turbo-preview",
                tools=[{"type": "retrieval"}],  # 启用文件检索工具
                instructions="""
                你是一个专业的文件搜索和分析助手。你的主要任务是：
                1. 理解用户的搜索意图
                2. 在上传的文件中搜索相关信息
                3. 提供准确、相关的答案
                4. 必要时引用原文内容
                5. 清晰地解释搜索结果
                """
            )
            
            # 创建对话线程
            self.thread = await self.client.beta.threads.create()
            
            return {
                "success": True,
                "assistant_id": self.assistant.id,
                "thread_id": self.thread.id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        上传文件到OpenAI
        
        参数:
        - file_path: 文件路径
        """
        try:
            with open(file_path, "rb") as file:
                response = await self.client.files.create(
                    file=file,
                    purpose="assistants"
                )
                
                self.uploaded_files.append(response.id)
                
                # 将文件附加到助手
                await self.client.beta.assistants.files.create(
                    assistant_id=self.assistant.id,
                    file_id=response.id
                )
                
                return {
                    "success": True,
                    "file_id": response.id
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def search_in_files(self, query: str) -> Dict[str, Any]:
        """
        在上传的文件中搜索信息
        
        参数:
        - query: 搜索查询
        """
        try:
            # 创建消息
            message = await self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=query
            )
            
            # 运行助手
            run = await self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # 等待处理完成
            while True:
                run_status = await self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
                
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    raise Exception(f"处理失败: {run_status.status}")
                
                await asyncio.sleep(1)
            
            # 获取回复
            messages = await self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            # 获取最新的助手回复
            assistant_messages = [
                msg for msg in messages.data 
                if msg.role == "assistant" and msg.run_id == run.id
            ]
            
            if assistant_messages:
                latest_message = assistant_messages[0]
                return {
                    "success": True,
                    "response": latest_message.content[0].text.value,
                    "message_id": latest_message.id
                }
            else:
                return {
                    "success": False,
                    "error": "没有找到助手的回复"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def cleanup(self) -> None:
        """
        清理资源
        """
        try:
            # 删除上传的文件
            for file_id in self.uploaded_files:
                await self.client.files.delete(file_id)
            
            # 删除助手
            if self.assistant:
                await self.client.beta.assistants.delete(self.assistant.id)
            
            # 删除线程
            if self.thread:
                await self.client.beta.threads.delete(self.thread.id)
                
        except Exception as e:
            print(f"清理资源时出错: {str(e)}")

async def demonstrate_file_search():
    """
    演示文件搜索功能
    """
    assistant = FileSearchAssistant()
    
    try:
        # 设置助手
        print("正在设置文件搜索助手...")
        setup_result = await assistant.setup_assistant()
        if not setup_result["success"]:
            raise Exception(f"设置助手失败: {setup_result['error']}")
        
        # 上传测试文件
        print("\n正在上传测试文件...")
        test_files = [
            "docs/python_guide.txt",
            "docs/machine_learning.pdf",
            "docs/api_documentation.md"
        ]
        
        for file_path in test_files:
            if os.path.exists(file_path):
                result = await assistant.upload_file(file_path)
                if result["success"]:
                    print(f"成功上传文件: {file_path}")
                else:
                    print(f"上传文件失败 {file_path}: {result['error']}")
        
        # 测试搜索查询
        test_queries = [
            "Python中如何处理异常？",
            "机器学习的主要类型有哪些？",
            "API认证方法有哪些？"
        ]
        
        print("\n开始测试搜索查询...")
        for query in test_queries:
            print(f"\n问题: {query}")
            result = await assistant.search_in_files(query)
            
            if result["success"]:
                print("回答:", result["response"])
            else:
                print(f"搜索失败: {result['error']}")
        
        # 清理资源
        print("\n清理资源...")
        await assistant.cleanup()
        print("演示完成")
        
    except Exception as e:
        print(f"演示过程中出错: {str(e)}")
        await assistant.cleanup()
