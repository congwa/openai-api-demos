from openai import OpenAI
from typing import Dict, List, Any, Optional
import json
from pydantic import BaseModel, Field
import datetime
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

# 定义数据模型
class Address(BaseModel):
    street: str = Field(..., description="街道地址")
    city: str = Field(..., description="城市名称")
    country: str = Field(..., description="国家名称")
    postal_code: str = Field(..., description="邮政编码")

class Person(BaseModel):
    name: str = Field(..., description="人员姓名")
    age: int = Field(..., description="年龄", ge=0, le=150)
    email: Optional[str] = Field(None, description="电子邮件地址")
    address: Address = Field(..., description="居住地址")
    interests: List[str] = Field(default=[], description="兴趣爱好列表")
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="记录创建时间"
    )

def get_structured_output(
    input_text: str,
    output_format: BaseModel,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Dict[str, Any]:
    """
    生成结构化输出
    
    参数:
    - input_text: 输入文本
    - output_format: Pydantic模型类
    - temperature: 输出的随机性 (0-1)
    - max_tokens: 最大输出长度
    """
    try:
        # 获取模型的JSON schema
        schema = output_format.schema()
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个专业的数据结构化处理专家。
请严格按照提供的JSON schema格式输出结果。
确保所有必填字段都有值，并符合数据类型要求。
如果信息不完整，请合理推断或使用默认值。"""
                },
                {
                    "role": "user",
                    "content": f"""
请将以下文本转换为结构化数据：
{input_text}

请严格按照以下schema格式输出：
{json.dumps(schema, indent=2, ensure_ascii=False)}
"""
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={ "type": "json_object" }  # 强制JSON输出
        )
        
        # 解析输出
        result = json.loads(response.choices[0].message.content)
        
        # 验证结果
        validated_data = output_format.parse_obj(result)
        
        return {
            "success": True,
            "data": validated_data.dict(),
            "raw_response": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def demonstrate_complex_extraction(text: str = None) -> Dict[str, Any]:
    """
    演示复杂信息提取
    """
    if text is None:
        text = """
        张三是一名来自北京市朝阳区阳光街123号的35岁软件工程师。
        他喜欢编程、阅读和旅行。他的邮箱是zhangsan@example.com。
        """
    
    return get_structured_output(text, Person)

def batch_process_texts(texts: List[str]) -> List[Dict[str, Any]]:
    """
    批量处理多个文本
    """
    results = []
    for text in texts:
        result = get_structured_output(text, Person)
        results.append(result)
    return results

def custom_schema_extraction(
    text: str,
    schema_definition: Dict[str, Any]
) -> Dict[str, Any]:
    """
    使用自定义schema提取信息
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的数据提取专家。"
                },
                {
                    "role": "user",
                    "content": f"""
请从以下文本中提取信息，并按照指定的schema格式输出：
{text}

Schema定义：
{json.dumps(schema_definition, indent=2, ensure_ascii=False)}
"""
                }
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        return {
            "success": True,
            "data": json.loads(response.choices[0].message.content)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 