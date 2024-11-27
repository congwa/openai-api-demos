from openai import OpenAI
import json
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

def get_weather(location, unit="celsius"):
    """
    根据传入的城市名称返回天气信息
    这里使用字典模拟不同城市的天气数据
    实际应用中应该调用真实的天气API
    """
    weather_data = {
        "北京": {"temperature": 20, "condition": "晴天"},
        "上海": {"temperature": 25, "condition": "多云"},
        "广州": {"temperature": 30, "condition": "雨天"},
    }
    
    # 获取指定城市的天气，如果城市不存在返回默认值
    return weather_data.get(location, {"temperature": 20, "condition": "未知"})

def chat_with_function(user_question):
    """
    处理用户的天气查询请求
    参数 user_question: 用户的问题，例如"北京今天的天气怎么样？"
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的天气助手"},
            {"role": "user", "content": user_question}  # 使用传入的问题
        ],
        # 通过函数调用机制，可以让GPT模型以结构化的方式请求所需信息
        # 天气数据获取和自然语言生成分开处理
        functions=[{
            "name": "get_weather",
            "description": "获取指定位置的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海、广州"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["location"]
            }
        }],
        function_call={"name": "get_weather"}
    )
    
    # 解析模型返回的函数调用参数
    # 模型会自动从用户问题中提取出需要的参数（如地点）
    function_args = json.loads(
        response.choices[0].message.function_call.arguments
    )
    
    # 使用解析出的参数调用天气函数获取数据
    weather_data = get_weather(**function_args)
    
    # 第二次调用API，让GPT基于天气数据生成自然语言回答
    # 这次包含了完整的对话历史和函数返回的数据
    second_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # 包含原始用户问题
            {"role": "user", "content": user_question},
            # 包含第一次GPT的回应（包含函数调用）
            response.choices[0].message,
            # 包含函数返回的天气数据
            {
                "role": "function",
                "name": "get_weather",
                "content": json.dumps(weather_data)
            }
        ]
    )
    
    # 返回最终的自然语言回答
    return second_response.choices[0].message.content 