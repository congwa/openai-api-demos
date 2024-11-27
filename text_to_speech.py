from openai import OpenAI
client = OpenAI()

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