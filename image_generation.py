from openai import OpenAI
client = OpenAI()

# 生成图像
def generate_image():
    response = client.images.generate(
        model="dall-e-3",
        prompt="一只可爱的熊猫在吃竹子，背景是竹林，阳光透过竹叶",
        n=1,                    # 生成图片数量
        size="1024x1024",      # 支持 1024x1024, 512x512, 256x256
        quality="hd",          # 图片质量：standard 或 hd
        style="vivid",         # natural 或 vivid
        response_format="url"  # url 或 b64_json
    )
    return response.data[0].url

# 图像变体
def create_image_variation():
    response = client.images.create_variation(
        image=open("panda.png", "rb"),
        n=1,                    # 变体数量
        size="1024x1024",      # 输出尺寸
        response_format="url",  # 响应格式
        user="user_123"        # 用户标识符
    )
    return response.data[0].url 