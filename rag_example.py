from openai import OpenAI
from typing import List, Dict, Any
import numpy as np
print("正在导入必要模块...")
from sklearn.metrics.pairwise import cosine_similarity
print("模块导入完成！")
import os
import json

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

class RAGSystem:
    def __init__(self, documents: List[Dict[str, str]] = None):
        """
        初始化RAG系统
        
        参数:
        - documents: 文档列表，每个文档是包含'title'和'content'的字典
        """
        self.documents = documents or []
        self.embeddings_cache = {}  # 缓存文档的嵌入向量
        
    def add_document(self, title: str, content: str) -> None:
        """添加新文档到知识库"""
        self.documents.append({
            'title': title,
            'content': content
        })
        # 清除缓存，因为文档集已更新
        self.embeddings_cache = {}
        
    def get_embedding(self, text: str) -> List[float]:
        """获取文本的嵌入向量"""
        try:
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"获取嵌入向量时出错: {str(e)}")
            return []

    def retrieve_relevant_docs(
        self, 
        query: str, 
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        检索与查询最相关的文档
        
        参数:
        - query: 查询文本
        - top_k: 返回的最相关文档数量
        """
        try:
            # 获取查询的嵌入向量
            query_embedding = self.get_embedding(query)
            
            # 获取所有文档的嵌入向量
            doc_embeddings = []
            for doc in self.documents:
                doc_text = f"{doc['title']} {doc['content']}"
                if doc_text in self.embeddings_cache:
                    embedding = self.embeddings_cache[doc_text]
                else:
                    embedding = self.get_embedding(doc_text)
                    self.embeddings_cache[doc_text] = embedding
                doc_embeddings.append(embedding)
            
            # 计算相似度
            similarities = cosine_similarity(
                [query_embedding], 
                doc_embeddings
            )[0]
            
            # 获取最相关的文档
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            return [{
                'document': self.documents[idx],
                'similarity': similarities[idx]
            } for idx in top_indices]
            
        except Exception as e:
            print(f"检索相关文档时出错: {str(e)}")
            return []

    async def generate_answer(
        self, 
        query: str,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        生成增强的回答
        
        参数:
        - query: 用户查询
        - temperature: 生成温度
        """
        try:
            # 检索相关文档
            relevant_docs = self.retrieve_relevant_docs(query)
            
            # 构建上下文
            context = "\n\n".join([
                f"文档 '{doc['document']['title']}':\n{doc['document']['content']}"
                for doc in relevant_docs
            ])
            
            # 构建提示
            prompt = f"""基于以下参考文档回答问题。如果文档中没有相关信息，请说明无法回答。

参考文档：
{context}

问题：{query}

请提供详细的回答："""

            # 生成回答
            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的助手，善于基于参考文档提供准确的回答。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            
            return {
                "success": True,
                "answer": response.choices[0].message.content,
                "relevant_docs": relevant_docs
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def save_knowledge_base(self, file_path: str) -> bool:
        """保存知识库到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存知识库时出错: {str(e)}")
            return False

    def load_knowledge_base(self, file_path: str) -> bool:
        """从文件加载知识库"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            self.embeddings_cache = {}  # 清除缓存
            return True
        except Exception as e:
            print(f"加载知识库时出错: {str(e)}")
            return False 