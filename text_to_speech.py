from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

def generate_speech():
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="alloy",
        input="你好，我是一个AI助手。",
        speed=1.0,
        response_format="mp3",
        voice_engine="neural"
    )
    
    response.stream_to_file("output.mp3") 