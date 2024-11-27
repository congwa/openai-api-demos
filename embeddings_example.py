from openai import OpenAI
import numpy as np
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

def demonstrate_embeddings():
    """
    演示不同的嵌入参数和用例
    """
    # 1. 基础文本嵌入
    basic_response = client.embeddings.create(
        model="text-embedding-3-small",  # 较小模型，适合简单任务
        input="你好，世界",
        encoding_format="float",  # 默认格式，返回浮点数
    )
    print("基础嵌入维度:", len(basic_response.data[0].embedding))

    # 2. 批量文本嵌入
    batch_response = client.embeddings.create(
        model="text-embedding-3-large",  # 较大模型，更高准确度
        input=[
            "这是第一句话",
            "这是第二句话",
            "这是第三句话"
        ],
        dimensions=256,  # 指定输出维度（仅支持某些模型）
    )
    
    # 3. 计算文本相似度
    def calculate_similarity(embedding1, embedding2):
        # 使用余弦相似度
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
    
    # 获取两个句子的嵌入并计算相似度
    similar_texts_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[
            "我喜欢吃苹果",
            "我爱吃水果"
        ]
    )
    
    embedding1 = similar_texts_response.data[0].embedding
    embedding2 = similar_texts_response.data[1].embedding
    similarity = calculate_similarity(embedding1, embedding2)
    
    return {
        "basic_embedding_length": len(basic_response.data[0].embedding),
        "batch_embedding_length": len(batch_response.data[0].embedding),
        "text_similarity": similarity
    }

def search_documents(query, documents):
    """
    搜索文档函数
    Args:
        query: 查询文本
        documents: 要搜索的文档列表
    Returns:
        最相关的文档及其相似度分数
    """
    # 获取查询文本的嵌入
    query_embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = query_embedding_response.data[0].embedding

    # 获取所有文档的嵌入
    doc_embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=documents
    )
    
    # 计算相似度并返回最相关的文档
    similarities = []
    for i, doc_embedding in enumerate(doc_embedding_response.data):
        similarity = np.dot(query_embedding, doc_embedding.embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding.embedding)
        )
        similarities.append((documents[i], similarity))
    
    # 按相似度排序
    return sorted(similarities, key=lambda x: x[1], reverse=True)

# 使用示例
if __name__ == "__main__":
    results = demonstrate_embeddings()
    print(f"结果：{results}") 


    