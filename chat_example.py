from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

# 基础聊天示例
def basic_chat():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "你好！"}
        ],
        temperature=0.7,          # 控制随机性 (0-2)
        top_p=0.95,              # 核采样阈值
        n=1,                     # 生成的回复数量
        max_tokens=150,          # 最大令牌数
        presence_penalty=0.0,    # 降低模型重复同样主题的倾向 (-2.0 到 2.0)
        frequency_penalty=0.0,   # 降低模型重复相同词语的倾向 (-2.0 到 2.0)
        logit_bias={},           # 调整特定令牌的采样概率
        user="user_123"          # 用户标识符，用于监控和检测滥用
    )
    return response.choices[0].message.content

# 带有温度参数的聊天
def creative_chat():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "给我讲个故事"}
        ],
        temperature=1.2,         # 更高的创造性
        top_p=0.9,              # 更灵活的词语选择
        max_tokens=500,         # 允许更长的回复
        presence_penalty=0.6,    # 鼓励话题多样性
        frequency_penalty=0.3,   # 减少重复
        stop=["\n\n", "结束"],   # 自定义停止标记
    )
    return response.choices[0].message.content

# 流式响应
async def stream_chat():
    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "写一首诗"}],
        stream=True,
        temperature=0.8,
        max_tokens=200,
        presence_penalty=0.2,
        frequency_penalty=0.2,
        response_format={ "type": "text" }  # 指定响应格式
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="") 