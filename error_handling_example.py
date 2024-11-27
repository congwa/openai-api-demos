async def safe_api_wrapper(func, *args, **kwargs):
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except RateLimitError:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))
                continue
            raise
        except OpenAIError as e:
            print(f"OpenAI API错误: {str(e)}")
            raise
        except Exception as e:
            print(f"未预期的错误: {str(e)}")
            raise

# 使用包装器
result = await safe_api_wrapper(basic_chat) 