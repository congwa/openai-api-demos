from openai import OpenAI
from typing import Dict, List, Any, Union, Generator
import json
from enum import Enum
import numpy as np
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),  # 可选 OpenAI API 中的组织 ID
    timeout=30.0  # 默认超时时间
)

class OutputFormat(Enum):
    JSON = "json_object"
    TEXT = "text"

def generate_with_control(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    output_format: OutputFormat = OutputFormat.TEXT,
    seed: int = None,
    max_tokens: int = 500
) -> Dict[str, Any]:
    """
    使用精确控制的参数生成输出
    
    参数:
    - prompt: 输入提示
    - temperature: 输出随机性 (0-2)
    - top_p: 核采样阈值 (0-1)
    - frequency_penalty: 词频惩罚 (-2.0 到 2.0)
    - presence_penalty: 主题重复惩罚 (-2.0 到 2.0)
    - output_format: 输出格式（JSON或文本）
    - seed: 随机种子，用于复现结果
    - max_tokens: 最大输出长度
    """
    try:
        response_format = {"type": output_format.value} if output_format == OutputFormat.JSON else None
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的AI助手，专注于生成高质量、可控的输出。"
                },
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            max_tokens=max_tokens
        )
        
        content = response.choices[0].message.content
        return {
            "success": True,
            "content": json.loads(content) if output_format == OutputFormat.JSON else content,
            "finish_reason": response.choices[0].finish_reason
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def demonstrate_temperature_effects(prompt: str) -> Dict[str, List[str]]:
    """
    演示不同temperature值的效果
    """
    temperatures = [0.2, 0.5, 0.7, 1.0]
    results = {str(temp): [] for temp in temperatures}
    
    for temp in temperatures:
        # 生成多个样本以展示差异
        for _ in range(3):
            result = generate_with_control(prompt, temperature=temp)
            if result["success"]:
                results[str(temp)].append(result["content"])
    
    return results

def demonstrate_top_p_effects(prompt: str) -> Dict[str, List[str]]:
    """
    演示不同top_p值的效果
    """
    top_p_values = [0.1, 0.5, 0.9]
    results = {str(p): [] for p in top_p_values}
    
    for p in top_p_values:
        for _ in range(3):
            result = generate_with_control(prompt, top_p=p, temperature=0.7)
            if result["success"]:
                results[str(p)].append(result["content"])
    
    return results

def demonstrate_penalties(
    prompt: str,
    repetitive_prompt: bool = False
) -> Dict[str, Any]:
    """
    演示频率和存在惩罚的效果
    """
    # 基准生成（无惩罚）
    base_result = generate_with_control(
        prompt,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    # 频率惩罚
    freq_result = generate_with_control(
        prompt,
        frequency_penalty=1.0,
        presence_penalty=0.0
    )
    
    # 存在惩罚
    pres_result = generate_with_control(
        prompt,
        frequency_penalty=0.0,
        presence_penalty=1.0
    )
    
    # 组合惩罚
    combined_result = generate_with_control(
        prompt,
        frequency_penalty=0.8,
        presence_penalty=0.8
    )
    
    return {
        "baseline": base_result["content"] if base_result["success"] else None,
        "frequency_penalty": freq_result["content"] if freq_result["success"] else None,
        "presence_penalty": pres_result["content"] if pres_result["success"] else None,
        "combined_penalties": combined_result["content"] if combined_result["success"] else None
    }

def demonstrate_reproducibility(
    prompt: str,
    seed: int = 42,
    num_samples: int = 3
) -> Dict[str, List[str]]:
    """
    演示使用种子实现可重复性
    """
    results = {
        "with_seed": [],
        "without_seed": []
    }
    
    # 使用固定种子生成
    for _ in range(num_samples):
        result = generate_with_control(prompt, seed=seed)
        if result["success"]:
            results["with_seed"].append(result["content"])
    
    # 不使用种子生成
    for _ in range(num_samples):
        result = generate_with_control(prompt)
        if result["success"]:
            results["without_seed"].append(result["content"])
    
    return results

def analyze_output_consistency(outputs: List[str]) -> Dict[str, float]:
    """
    分析输出的一致性
    """
    from difflib import SequenceMatcher
    
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()
    
    similarities = []
    for i in range(len(outputs)):
        for j in range(i + 1, len(outputs)):
            similarities.append(similarity(outputs[i], outputs[j]))
    
    return {
        "mean_similarity": np.mean(similarities) if similarities else 0,
        "std_similarity": np.std(similarities) if similarities else 0,
        "min_similarity": min(similarities) if similarities else 0,
        "max_similarity": max(similarities) if similarities else 0
    }

async def generate_with_prediction(
    prompt: str,
    prediction_content: str = None,
    stream: bool = False,
    temperature: float = 0.7,
    max_tokens: int = 500
) -> Union[Dict[str, Any], Generator]:
    """
    使用prediction参数生成输出
    
    参数:
    - prompt: 输入提示
    - prediction_content: 预期的输出内容
    - stream: 是否使用流式输出
    - temperature: 输出随机性 (0-2)
    - max_tokens: 最大输出长度
    """
    try:
        messages = [{"role": "user", "content": prompt}]
        
        # 构建prediction参数
        prediction = None
        if prediction_content:
            prediction = {
                "type": "content",
                "content": prediction_content
            }
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            prediction=prediction,  # 添加prediction参数
            stream=stream          # 支持流式输出
        )
        
        if stream:
            return response
        else:
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "finish_reason": response.choices[0].finish_reason
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def demonstrate_prediction_streaming(
    code: str,
    refactor_prompt: str
) -> None:
    """
    演示带prediction的流式输出
    """
    try:
        stream = await generate_with_prediction(
            prompt=refactor_prompt,
            prediction_content=code,
            stream=True
        )
        
        print("开始流式输出:")
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
        print("\n流式输出完成")
        
    except Exception as e:
        print(f"流式输出错误: {str(e)}")

async def demonstrate_code_refactoring(
    original_code: str,
    modifications: List[str]
) -> Dict[str, Any]:
    """
    演示代码重构场景
    
    参数:
    - original_code: 原始代码
    - modifications: 修改说明列表
    """
    results = []
    
    for modification in modifications:
        result = await generate_with_prediction(
            prompt=f"按照以下要求修改代码：{modification}",
            prediction_content=original_code,
            temperature=0.3  # 使用较低的temperature以保持代码风格
        )
        results.append({
            "modification": modification,
            "result": result
        })
    
    return {
        "success": True,
        "results": results
    }

async def demonstrate_content_completion(
    partial_content: str,
    expected_completion: str
) -> Dict[str, Any]:
    """
    演示内容补全场景
    """
    try:
        result = await generate_with_prediction(
            prompt="请完成以下内容：",
            prediction_content=expected_completion,
            temperature=0.5
        )
        
        return {
            "success": True,
            "original": partial_content,
            "completion": result["content"] if result["success"] else None,
            "expected": expected_completion
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }