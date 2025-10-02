"""
基于 CrewAI 和 DeepSeek 模型的信息可视化应用
三阶段处理：内容提炼 -> 信息分析与结构化 -> 可视化决策与执行
"""

import os
import json
import re
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from datetime import datetime
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

# 配置 DeepSeek 模型
def get_deepseek_llm():
    """配置 DeepSeek 模型"""
    return ChatOpenAI(
        model="deepseek/deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        temperature=0.1
    )

# 获取 DeepSeek LLM 实例
deepseek_llm = get_deepseek_llm()

def extract_json_from_markdown(text: str) -> str:
    """从包含 markdown 代码块的文本中提取 JSON 内容"""
    if not text:
        return ""

    # 查找 ```json ... ``` 格式的内容
    json_pattern = r'```json\s*\n(.*?)\n```'
    match = re.search(json_pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()

    # 如果没有找到 ```json 格式，尝试查找纯 JSON 内容
    # 查找第一个 { 到最后一个 } 之间的内容
    json_pattern = r'\{.*\}'
    match = re.search(json_pattern, text, re.DOTALL)

    if match:
        return match.group(0).strip()

    # 如果都没找到，返回原文本
    return text

def validate_data_authenticity(result_data: str, original_text: str) -> Dict[str, Any]:
    """验证生成的数据是否包含虚拟数据"""
    warnings = []

    try:
        # 尝试解析JSON数据
        if result_data.strip():
            data = json.loads(result_data)

            # 检查可视化数据
            if 'visualizations' in data:
                for viz in data['visualizations']:
                    if viz.get('type') == 'echarts' and 'config' in viz:
                        config = viz['config']

                        # 检查雷达图数据
                        if 'radar' in config:
                            series_data = config.get('series', [])
                            for series in series_data:
                                if 'data' in series:
                                    for data_item in series['data']:
                                        if 'value' in data_item:
                                            values = data_item['value']
                                            # 检查是否包含虚拟数值（如85, 70, 45等常见虚拟权重）
                                            if any(val in [85, 70, 45, 90, 80, 60, 50, 40, 30, 20, 10] for val in values):
                                                warnings.append(f"检测到可能的虚拟数据：雷达图权重 {values}")

                        # 检查饼图数据
                        if 'series' in config:
                            for series in config['series']:
                                if series.get('type') == 'pie' and 'data' in series:
                                    pie_data = series['data']
                                    # 检查是否包含虚拟百分比数据
                                    for item in pie_data:
                                        if 'value' in item and isinstance(item['value'], (int, float)):
                                            if item['value'] in [85, 70, 45, 90, 80, 60, 50, 40, 30, 20, 10]:
                                                warnings.append(f"检测到可能的虚拟数据：饼图数值 {item['value']}")

            # 检查关键指标数据
            if 'key_metrics' in data:
                for metric in data['key_metrics']:
                    if 'value' in metric:
                        value = metric['value']
                        # 检查是否包含虚拟权重值
                        if isinstance(value, (int, float)) and value in [85, 70, 45, 90, 80, 60, 50, 40, 30, 20, 10]:
                            warnings.append(f"检测到可能的虚拟数据：关键指标数值 {value}")

    except json.JSONDecodeError:
        warnings.append("无法解析JSON数据，跳过虚拟数据检查")

    return {
        "has_virtual_data": len(warnings) > 0,
        "warnings": warnings,
        "original_text_length": len(original_text),
        "result_data_length": len(result_data)
    }

# 创建 Agent
information_processor = Agent(
    role="信息处理专家",
    goal="通读文章，识别并提取核心论点、关键数据和重要实体，然后进行归纳、分类，并转换为适合可视化的结构化数据",
    backstory="你是一位专业的信息处理专家，既擅长从复杂文本中提取关键信息，又精通将非结构化信息转换为结构化数据。你能够：\n"
              "1. 深度分析文本内容，识别核心论点、关键数据和重要实体\n"
              "2. 对提取的信息进行归纳、分类和结构化处理\n"
              "3. 将处理后的信息转换为适合可视化的JSON格式数据\n"
              "4. 确保数据的完整性和逻辑性，为后续可视化提供高质量的结构化数据\n"
              "**重要约束：绝对禁止生成任何虚拟、推测或虚构的数据，所有数据必须严格来源于原始文本**",
    llm=deepseek_llm,
    verbose=True
)

visualizer = Agent(
    role="可视化工程师",
    goal="根据数据结构智能选择最合适的可视化类型，生成 Card 卡片展示和 ECharts 图表配置，确保数据故事完整性和可视化效果最佳",
    backstory="你是一位资深的数据可视化专家，精通各种图表类型和可视化最佳实践。你能够：\n"
              "1. 分析数据特征，识别关键洞察点\n"
              "2. 智能选择最适合的可视化类型：Card 卡片展示（适合摘要信息）或 ECharts 图表（适合数据可视化）\n"
              "3. 生成 Card 卡片：包含标题、摘要、关键数据点，适合快速信息概览\n"
              "4. 生成 ECharts 配置：柱状图、折线图、饼图、雷达图等，适合详细数据分析\n"
              "5. 确保不同可视化类型间的逻辑关联性和视觉一致性\n"
              "6. 考虑用户交互体验和内容可读性\n"
              "**严格约束：绝对禁止生成任何虚拟、推测或虚构的数据，所有图表数据必须严格来源于输入的结构化数据，不得添加任何原始数据中不存在的数值、比例或权重**",
    llm=deepseek_llm,
    verbose=True
)

def process_text_with_crewai(text: str) -> Dict[str, Any]:
    """使用 CrewAI 处理文本信息可视化"""

    information_processing_task = Task(
        description=f"请分析以下文本内容，完成信息提取和结构化处理：\n\n{text}\n\n"
                   "请按以下步骤执行：\n"
                   "1. 深度分析文本内容，识别核心论点、关键数据和重要实体\n"
                   "2. 对提取的信息进行归纳、分类和结构化处理\n"
                   "3. 将处理后的信息转换为适合可视化的JSON格式数据\n"
                   "4. 确保数据的完整性和逻辑性\n"
                   "**严格约束：绝对禁止生成任何虚拟、推测或虚构的数据，所有数据必须严格来源于原始文本，不得添加任何原始文本中不存在的数值、比例或权重**",
        agent=information_processor,
        expected_output="结构化的 JSON 数据，包含实体、指标、分类等信息，以及信息提取的详细报告。所有数据必须严格来源于原始文本。"
    )

    visualization_task = Task(
        description="基于信息处理专家提供的结构化数据，进行深度分析并生成多种类型的可视化展示。\n"
                   "请按以下步骤执行：\n"
                   "1. 分析数据结构，识别关键数据维度和关系\n"
                   "2. 智能选择可视化类型：\n"
                   "   - Card 卡片：适合展示摘要信息、关键数据点、核心论点\n"
                   "   - ECharts 图表：适合展示详细数据分析和趋势\n"
                   "3. 为 Card 卡片生成：标题、摘要、关键数据点、核心洞察\n"
                   "4. 为 ECharts 图表选择最适合的类型（柱状图、折线图、饼图、散点图等）\n"
                   "5. 确保不同可视化类型间有逻辑关联，形成完整的数据分析报告\n"
                   "6. **重要：严格避免内容重复，确保每个可视化项都有独特的价值：\n"
                   "   - 卡片之间：避免相同数据点的重复展示，每个卡片应聚焦不同维度\n"
                   "   - 图表之间：避免相同数据的不同展示形式，每个图表应展示不同的分析角度\n"
                   "   - 卡片与图表：避免数据重复，卡片展示摘要，图表展示详细分析\n"
                   "   - 内容差异化：每个可视化项应提供独特的信息价值，避免冗余\n"
                   "7. 内容分配策略：\n"
                   "   - 第一个卡片：核心摘要和总体趋势\n"
                   "   - 第二个卡片：关键指标和重要发现（与第一个卡片不重复）\n"
                   "   - 第一个图表：时间序列分析或趋势对比\n"
                   "   - 第二个图表：分类分析或结构分析（与第一个图表不重复）\n"
                   "   - 第三个图表：影响因素分析或相关性分析（与前两个图表不重复）\n"
                   "8. **严格约束：绝对禁止生成任何虚拟、推测或虚构的数据：\n"
                   "   - 所有图表数据必须严格来源于输入的结构化数据\n"
                   "   - 不得添加任何原始数据中不存在的数值、比例或权重\n"
                   "   - 如果原始数据中没有量化权重，不得生成雷达图等需要数值权重的图表\n"
                   "   - 如果原始数据中没有百分比数据，不得生成饼图等需要比例数据的图表\n"
                   "   - 优先选择能够直接使用原始数据的图表类型（如折线图、柱状图）\n",
        agent=visualizer,
        expected_output="包含可视化项的JSON对象：\n"
                       "visualizations: 可视化项数组，每个项包含：\n"
                       "1. Card 卡片配置：\n"
                       "   - type: 'card'\n"
                       "   - card_id: 卡片唯一标识\n"
                       "   - title: 卡片标题（确保与其他卡片标题不重复）\n"
                       "   - summary: 摘要内容（确保与其他卡片内容不重复）\n"
                       "   - key_points: 关键数据点列表（确保数据点不重复）\n"
                       "   - insights: 核心洞察（确保洞察角度不重复）\n"
                       "2. ECharts 图表配置：\n"
                       "   - type: 'echarts'\n"
                       "   - chart_id: 图表唯一标识\n"
                       "   - title: 图表标题（确保与其他图表标题不重复）\n"
                       "   - config: 完整的ECharts配置，不需要包含color相关配置，不允许出现javascript函数\n"
                       "**严格数据约束：\n"
                       "- 所有图表数据必须严格来源于输入的结构化数据\n"
                       "- 绝对禁止生成任何虚拟、推测或虚构的数据\n"
                       "- 不得添加任何原始数据中不存在的数值、比例或权重\n"
                       "- 如果原始数据中没有量化权重，不得生成雷达图等需要数值权重的图表\n"
                       "- 如果原始数据中没有百分比数据，不得生成饼图等需要比例数据的图表\n"
                       "- 优先选择能够直接使用原始数据的图表类型（如折线图、柱状图）\n"
                       "**去重要求：\n"
                       "- 每个可视化项必须有独特的信息价值\n"
                       "- 避免相同数据在不同可视化项中重复展示\n"
                       "- 确保卡片和图表之间的内容互补而非重复\n"
                       "- 每个可视化项应聚焦不同的分析维度或数据角度\n",
        context=[information_processing_task]
    )

    crew = Crew(
        agents=[information_processor, visualizer],
        tasks=[information_processing_task, visualization_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    return {
        "information_processing_result": str(information_processing_task.output) if information_processing_task.output else "未完成",
        "visualization_result": extract_json_from_markdown(str(visualization_task.output)) if visualization_task.output else "未完成",
        "final_result": extract_json_from_markdown(str(result)) if result else "未完成"
    }

def main():
    """主程序入口"""
    print("🚀 启动基于 CrewAI 和 DeepSeek 的信息可视化应用")

    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 请设置 DEEPSEEK_API_KEY 环境变量")
        return

    try:
        with open('data.txt', 'r', encoding='utf-8') as f:
            text_content = f.read()
        print(f"📄 已读取数据文件，内容长度: {len(text_content)} 字符")
    except FileNotFoundError:
        print("❌ 未找到 data.txt 文件")
        return

    print("\n🔄 开始 CrewAI 三阶段处理...")

    try:
        results = process_text_with_crewai(text_content)
        print("\n✅ 处理完成！")

        # 验证数据真实性
        print("\n🔍 验证数据真实性...")
        validation_result = validate_data_authenticity(
            results.get('visualization_result', ''),
            text_content
        )

        if validation_result['has_virtual_data']:
            print("⚠️  警告：检测到可能的虚拟数据！")
            for warning in validation_result['warnings']:
                print(f"   - {warning}")
            print("💡 建议：请检查生成的可视化数据是否严格来源于原始文本")
        else:
            print("✅ 数据验证通过：未检测到虚拟数据")

        # 保存结果
        serializable_results = {
            "information_processing_result": str(results.get('information_processing_result', '')),
            "visualization_result": str(results.get('visualization_result', '')),
            "final_result": str(results.get('final_result', '')),
            "data_validation": validation_result,
            "timestamp": str(datetime.now())
        }

        with open('visualization_result.json', 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存到: visualization_result.json")

    except Exception as e:
        print(f"❌ 处理过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

