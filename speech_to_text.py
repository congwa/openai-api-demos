from openai import OpenAI
client = OpenAI()

def transcribe_audio():
    audio_file = open("speech.mp3", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="zh",           # 音频语言
        prompt="这是一段中文演讲", # 提示词以提高准确性
        response_format="text",  # text, json, srt, verbose_json, vtt
        temperature=0.2,        # 控制随机性
        timestamp_granularities=["word", "segment"]  # 时间戳粒度
    )
    return transcript.text 