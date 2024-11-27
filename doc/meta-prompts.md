# 元提示

元提示提示词生成的一部分， 可以用来生成提示词

核心功能：
元提示生成
提示测试
提示优化
示例场景：
代码审查助手
文章摘要生成器
提示结构：
主要指令
上下文信息
输入/输出格式
示例
约束条件
评估标准

使用方法：
# 基础使用
generator = MetaPromptGenerator()
result = await generator.generate_meta_prompt(
    task_description="你的任务描述",
    constraints=["约束1", "约束2"]
)

# 测试提示
test_result = await generator.test_generated_prompt(
    result["prompt"],
    ["测试输入1", "测试输入2"]
)

# 优化提示
refined_result = await generator.refine_prompt(
    result["prompt"],
    "优化建议"
最佳实践：
提供清晰的任务描述
包含具体的约束条件
添加示例输入输出
指定目标受众
进行提示测试
基于反馈优化
这个实现提供了完整的元提示生成和优化功能，可以根据具体需求进行调整和扩展。

