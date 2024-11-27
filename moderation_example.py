from openai import OpenAI
from typing import List, Dict, Union

client = OpenAI()

def demonstrate_moderation(texts: Union[str, List[str]] = None) -> Dict:
    """
    演示OpenAI的内容审核功能
    支持单个文本或文本列表的审核
    """
    if texts is None:
        texts = [
            "我爱和平与友善",  # 正常文本
            "我要杀了你",      # 暴力内容
            "我恨所有人",      # 仇恨言论
            "毒品在哪里买",    # 违禁品相关
            "性感美女电话",    # 成人内容
        ]

    try:
        # 调用审核API
        response = client.moderations.create(
            input=texts,
            model="text-moderation-latest"  # 使用最新模型
        )
        
        # 解析结果
        results = []
        for idx, result in enumerate(response.results):
            analysis = {
                "文本": texts[idx],
                "违规": result.flagged,
                "违规类别": {
                    "暴力": result.categories.violence,
                    "性相关": result.categories.sexual,
                    "仇恨": result.categories.hate,
                    "自残": result.categories.self_harm,
                    "色情": result.categories.sexual_minors,
                    "骚扰": result.categories.harassment,
                    "违禁品": result.categories.violence_graphic,
                },
                "违规分数": {
                    "暴力": result.category_scores.violence,
                    "性相关": result.category_scores.sexual,
                    "仇恨": result.category_scores.hate,
                    "自残": result.category_scores.self_harm,
                    "色情": result.category_scores.sexual_minors,
                    "骚扰": result.category_scores.harassment,
                    "违禁品": result.category_scores.violence_graphic,
                }
            }
            results.append(analysis)
        
        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def filter_safe_content(texts: List[str]) -> List[str]:
    """
    过滤内容，只返回安全的文本
    """
    response = client.moderations.create(
        input=texts,
        model="text-moderation-latest"
    )
    
    safe_texts = [
        text for text, result in zip(texts, response.results)
        if not result.flagged
    ]
    
    return safe_texts 