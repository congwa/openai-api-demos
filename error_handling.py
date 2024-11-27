from openai import OpenAI, OpenAIError, RateLimitError, APIError, Timeout

client = OpenAI()

def safe_api_call():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "你好"}],
            timeout=30,          # 请求超时时间
            request_timeout=30,  # HTTP请求超时
            max_retries=3       # 最大重试次数
        )
        return response.choices[0].message.content
    except RateLimitError as e:
        print(f"达到速率限制: {str(e)}")
        return None
    except Timeout as e:
        print(f"请求超时: {str(e)}")
        return None
    except APIError as e:
        print(f"API错误: {str(e)}")
        return None
    except OpenAIError as e:
        print(f"其他OpenAI错误: {str(e)}")
        return None
    except Exception as e:
        print(f"未预期的错误: {str(e)}")
        return None 