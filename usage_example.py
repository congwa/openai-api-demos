# 单独使用聊天功能
response = basic_chat()

# 生成图片并保存
image_url = generate_image()
# 可以使用requests下载图片
import requests
image_data = requests.get(image_url).content
with open("generated_image.png", "wb") as f:
    f.write(image_data)

# 语音处理链
def process_voice_chain():
    # 1. 先将文字转换为语音
    generate_speech()
    # 2. 再将生成的语音转换回文字
    transcript = transcribe_audio()
    return transcript

# 天气查询示例
weather_info = chat_with_function() 