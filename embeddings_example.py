from openai import OpenAI
import numpy as np

client = OpenAI()

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

# 使用示例
if __name__ == "__main__":
    results = demonstrate_embeddings()
    print(f"结果：{results}") 


    