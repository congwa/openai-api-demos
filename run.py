from chat_example import basic_chat, creative_chat, stream_chat
from function_calling import chat_with_function
from image_generation import generate_image, create_image_variation
from speech_to_text import transcribe_audio
from text_to_speech import generate_speech
from error_handling import safe_api_call
from embeddings_example import demonstrate_embeddings, search_documents
from moderation_example import demonstrate_moderation, filter_safe_content
from reasoning_example import demonstrate_cot_reasoning, solve_complex_task, demonstrate_step_by_step_coding
from vision_example import (
    analyze_image, 
    analyze_multiple_images, 
    analyze_image_with_specific_focus
)
from structured_output_example import (
    demonstrate_complex_extraction,
    batch_process_texts,
    custom_schema_extraction
)
from predicted_outputs_example import (
    demonstrate_temperature_effects,
    demonstrate_top_p_effects,
    demonstrate_penalties,
    demonstrate_reproducibility,
    analyze_output_consistency,
    demonstrate_code_refactoring,
    demonstrate_prediction_streaming,
    demonstrate_content_completion
)
from rag_example import RAGSystem
from tools.file_search_example import FileSearchAssistant
from meta_prompts_example import demonstrate_meta_prompts
import argparse
import json
import os

async def demo_all_features():
    try:
        print("=== 1. 基础聊天演示 ===")
        chat_response = basic_chat()
        print(f"基础聊天响应: {chat_response}\n")

        print("=== 2. 创意聊天演示 ===")
        creative_response = creative_chat()
        print(f"创意聊天响应: {creative_response}\n")

        print("=== 3. 流式聊天演示 ===")
        print("开始流式输出诗歌:")
        await stream_chat()
        print("\n")

        print("=== 4. 函数调用演示 ===")
        weather_response = chat_with_function()
        print(f"天气查询结果: {weather_response}\n")

        print("=== 5. 图像生成演示 ===")
        image_url = generate_image()
        print(f"生成的图片URL: {image_url}\n")

        # 假设我们已经有了一张熊猫图片
        if os.path.exists("panda.png"):
            variation_url = create_image_variation()
            print(f"图片变体URL: {variation_url}\n")

        print("=== 6. 语音转文字演示 ===")
        # 假设我们有语音文件
        if os.path.exists("speech.mp3"):
            transcript = transcribe_audio()
            print(f"转录结果: {transcript}\n")

        print("=== 7. 文字转语音演示 ===")
        generate_speech()
        print("语音文件已生成: output.mp3\n")

        print("=== 8. 错误处理演示 ===")
        safe_response = safe_api_call()
        print(f"安全调用响应: {safe_response}\n")

        print("=== 9. 文本嵌入演示 ===")
        # 基础嵌入演示
        embedding_results = demonstrate_embeddings()
        print(f"基础嵌入维度: {embedding_results['basic_embedding_length']}")
        print(f"批量嵌入维度: {embedding_results['batch_embedding_length']}")
        print(f"文本相似度: {embedding_results['text_similarity']:.4f}\n")

        # 文档搜索示例
        documents = [
            "机器学习是人工智能的一个子领域",
            "深度学习是机器学习的一种方法",
            "自然语言处理是人工智能的重要应用",
            "计算机视觉主要处理图像和视频数据"
        ]
        query = "什么是机器学习"
        best_match_index = search_documents(query, documents)
        print(f"搜索查询: {query}")
        print(f"最相关的文档: {documents[best_match_index]}\n")

        print("=== 10. 内容审核演示 ===")
        # 基础审核演示
        moderation_results = demonstrate_moderation()
        if moderation_results["success"]:
            print("\n=== 内容审核结果 ===")
            for result in moderation_results["results"]:
                print(f"\n文本: {result['文本']}")
                print(f"违规: {'是' if result['违规'] else '否'}")
                if result['违规']:
                    print("违规类别:")
                    for category, is_flagged in result['违规类别'].items():
                        if is_flagged:
                            score = result['违规分数'][category]
                            print(f"- {category}: {score:.3f}")

        # 内容过滤示例
        test_texts = [
            "今天天气真好",
            "我要杀了你",
            "让我们一起学习",
            "毒品在哪里买"
        ]
        safe_texts = filter_safe_content(test_texts)
        print("\n=== 安全内容过滤结果 ===")
        print("原始文本:", test_texts)
        print("安全文本:", safe_texts)

        print("=== 11. 推理能力演示 ===")
        
        # Chain of Thought 演示
        print("\n=== 链式思维解题示例 ===")
        math_result = demonstrate_cot_reasoning()
        if math_result["success"]:
            print(math_result["reasoning"])

        # 系统设计推理演示
        print("\n=== 系统设计推理示例 ===")
        design_result = solve_complex_task()
        if design_result["success"]:
            print(design_result["design"])

        # 编程问题解决演示
        print("\n=== 编程问题解决示例 ===")
        coding_result = demonstrate_step_by_step_coding()
        if coding_result["success"]:
            print(coding_result["solution"])

        print("=== 12. 视觉分析演示 ===")
        
        # 基础图片分析
        print("\n=== 单图分析示例 ===")
        image_path = "panda.png"
        if os.path.exists(image_path):
            result = analyze_image(
                image_path,
                prompt="这张图片展示了什么？",
                detail_level="high"
            )
            if result["success"]:
                print(result["analysis"])

        # 多图比较分析
        print("\n=== 多图比较示例 ===")
        image_paths = ["panda1.png", "panda2.png"]
        if all(os.path.exists(path) for path in image_paths):
            result = analyze_multiple_images(
                image_paths,
                prompt="请比较这两张图片的主要区别"
            )
            if result["success"]:
                print(result["comparison"])

        # 特定焦点分析
        print("\n=== 特定焦点分析示例 ===")
        if os.path.exists(image_path):
            result = analyze_image_with_specific_focus(
                image_path,
                focus_areas=["颜色搭配", "构图技巧", "情感表达"]
            )
            if result["success"]:
                print(result["focused_analysis"])

        print("=== 13. 结构化输出演示 ===")
        
        # 基础信息提取
        print("\n=== 基础信息提取示例 ===")
        text = """
        李四是一名28岁的医生，住在上海市浦东新区阳光路456号。
        他喜欢打篮球和游泳，邮箱是lisi@example.com。
        """
        result = demonstrate_complex_extraction(text)
        if result["success"]:
            print(json.dumps(result["data"], indent=2, ensure_ascii=False))

        # 批量处理
        print("\n=== 批量处理示例 ===")
        texts = [
            "王五，42岁，居住地：广州市天河区月亮街789号，爱好：钓鱼、摄影",
            "赵六，31岁，居住地：深市南山区星光路321号，爱好：烹饪、旅行"
        ]
        results = batch_process_texts(texts)
        for idx, result in enumerate(results, 1):
            if result["success"]:
                print(f"\n文本 {idx} 的提取结果：")
                print(json.dumps(result["data"], indent=2, ensure_ascii=False))

        # 自定义Schema提取
        print("\n=== 自定义Schema提取示例 ===")
        custom_schema = {
            "type": "object",
            "properties": {
                "产品名称": {"type": "string"},
                "价格": {"type": "number"},
                "规格": {
                    "type": "object",
                    "properties": {
                        "尺寸": {"type": "string"},
                        "重量": {"type": "string"},
                        "颜色": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        }
        product_text = """
        新款智能手机X100，售价4999元，
        尺寸：158.3x73.2x8.2mm，重量189g，
        有暗夜黑、极光蓝、珍珠白三种颜色可选。
        """
        custom_result = custom_schema_extraction(product_text, custom_schema)
        if custom_result["success"]:
            print(json.dumps(custom_result["data"], indent=2, ensure_ascii=False))

        print("=== 14. 预测输出控制演示 ===")
        
        # Temperature效果演示
        print("\n=== Temperature效果示例 ===")
        prompt = "给我讲一个关于太空探险的短故事"
        temp_results = demonstrate_temperature_effects(prompt)
        for temp, outputs in temp_results.items():
            print(f"\nTemperature = {temp}:")
            for idx, output in enumerate(outputs, 1):
                print(f"样本 {idx}:\n{output[:100]}...")
            
            # 分析输出一致性
            consistency = analyze_output_consistency(outputs)
            print(f"一致性分析: 平均相似度 = {consistency['mean_similarity']:.2f}")

        # Top-p效果演示
        print("\n=== Top-p效果示例 ===")
        top_p_results = demonstrate_top_p_effects(prompt)
        for p, outputs in top_p_results.items():
            print(f"\nTop-p = {p}:")
            for idx, output in enumerate(outputs, 1):
                print(f"样本 {idx}:\n{output[:100]}...")

        # 惩罚效果演示
        print("\n=== 惩罚效果示例 ===")
        repetitive_prompt = "列出5个编程语言的优点"
        penalty_results = demonstrate_penalties(repetitive_prompt, True)
        for penalty_type, output in penalty_results.items():
            print(f"\n{penalty_type}:\n{output[:200]}...")

        # 可重复性演示
        print("\n=== 可重复性示例 ===")
        seed_results = demonstrate_reproducibility(prompt)
        print("\n使用固定种子:")
        for idx, output in enumerate(seed_results["with_seed"], 1):
            print(f"生成 {idx}:\n{output[:100]}...")
        
        print("\n不使用种子:")
        for idx, output in enumerate(seed_results["without_seed"], 1):
            print(f"生成 {idx}:\n{output[:100]}...")

        print("\n=== Prediction参数演示 ===")
        
        # 代码重构示例
        print("\n1. 代码重构示例")
        original_code = """
class User {
    firstName: string = "";
    lastName: string = "";
    username: string = "";
}
        """.strip()
        
        modifications = [
            "将username替换为email",
            "添加一个age属性",
            "添加一个getFullName方法"
        ]
        
        refactor_results = await demonstrate_code_refactoring(
            original_code,
            modifications
        )
        
        if refactor_results["success"]:
            for result in refactor_results["results"]:
                print(f"\n修改要求: {result['modification']}")
                if result["result"]["success"]:
                    print("修改后的代码:")
                    print(result["result"]["content"])

        # 流式输出示例
        print("\n2. 流式输出示例")
        refactor_prompt = "将username属性替换为email属性"
        await demonstrate_prediction_streaming(
            original_code,
            refactor_prompt
        )

        # 内容补全示例
        print("\n3. 内容补全示例")
        partial_content = "OpenAI是一家"
        expected_completion = "OpenAI是一家专注于人工智能研究的公司"
        
        completion_result = await demonstrate_content_completion(
            partial_content,
            expected_completion
        )
        
        if completion_result["success"]:
            print(f"原始内容: {completion_result['original']}")
            print(f"补全结果: {completion_result['completion']}")
            print(f"预期结果: {completion_result['expected']}")

        print("=== 15. RAG系统演示 ===")
        
        # 初始化RAG系统
        rag = RAGSystem()
        
        # 添加示例文档
        documents = [
            {
                "title": "Python简介",
                "content": "Python是一种高级编程语言，以其简洁的语法和丰富的库而闻名。它支持多种编程范式，包括面向对象、命令式和函数式编程。"
            },
            {
                "title": "机器学习基础",
                "content": "机器学习是人工智能的一个子领域，它使计算机系统能够通过经验自动改进。常见的机器学习方法包括监督学习、无监督学习和强化学习。"
            },
            {
                "title": "深度学习简介",
                "content": "深度学习是机器学习的一个分支，使用多层神经网络进行特征学习和模式识别。它在图像识别、自然语言处理等领域取得了突破性进展。"
            }
        ]
        
        for doc in documents:
            rag.add_document(doc["title"], doc["content"])
        
        # 保存知识库
        rag.save_knowledge_base("output/knowledge_base.json")
        
        # 测试查询
        queries = [
            "什么是Python？",
            "机器学习和深度学习有什么关系？",
            "量子计算机是什么？"  # 知识库中没有的信息
        ]
        
        for query in queries:
            print(f"\n问题: {query}")
            result = await rag.generate_answer(query)
            
            if result["success"]:
                print("\n回答:", result["answer"])
                print("\n相关文档:")
                for doc in result["relevant_docs"]:
                    print(f"- {doc['document']['title']} (相似度: {doc['similarity']:.3f})")
            else:
                print(f"生成回答时出错: {result['error']}")

        print("\n=== 16. 文件搜索助手演示 ===")
        assistant = FileSearchAssistant(client)
        
        # 设置助手
        print("正在设置文件搜索助手...")
        setup_result = await assistant.setup_assistant()
        if not setup_result["success"]:
            raise Exception(f"设置助手失败: {setup_result['error']}")
        
        # 上传测试文件
        print("\n正在上传测试文件...")
        test_files = [
            "tools/docs/python_guide.txt",
            "tools/docs/machine_learning.pdf",
            "tools/docs/api_documentation.md"
        ]
        
        for file_path in test_files:
            result = await assistant.upload_file(file_path)
            if result["success"]:
                print(f"成功上传文件: {file_path}")
            else:
                print(f"上传文件失败 {file_path}: {result['error']}")
        
        # 测试搜索查询
        test_queries = [
            "Python中如何处理异常？请给出示例代码",
            "机器���习的主要类���有哪些？每种类型的特点是什么？",
            "API认证有哪些主要方法？请详细说明每种方法的特点"
        ]
        
        print("\n开始测试文件搜索...")
        for query in test_queries:
            print(f"\n问题: {query}")
            result = await assistant.search_in_files(query)
            
            if result["success"]:
                print("\n回答:", result["response"])
            else:
                print(f"搜索失败: {result['error']}")
        
        # 清理资源
        print("\n清理资源...")
        await assistant.cleanup()
        print("文件搜索演示完成")

        print("\n=== 17. 元提示生成演示 ===")
        await demonstrate_meta_prompts()

    except Exception as e:
        print(f"发生错误: {str(e)}")
