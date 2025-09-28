"""
基于 CrewAI 和 DeepSeek 模型的信息可视化应用
三阶段处理：内容提炼 -> 信息分析与结构化 -> 可视化决策与执行
"""

import os
import json
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from tools import ContentExtractionTool, DataStructuringTool, VisualizationTool
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


# 创建工具实例
content_extraction_tool = ContentExtractionTool()
data_structuring_tool = DataStructuringTool()
visualization_tool = VisualizationTool()

# 获取 DeepSeek LLM 实例
deepseek_llm = get_deepseek_llm()

# 创建 Agent
researcher = Agent(
    role="研究员",
    goal="通读文章，识别并提取核心论点、关键数据和重要实体",
    backstory="你是一位专业的研究员，擅长从复杂文本中提取关键信息。",
    tools=[content_extraction_tool],
    llm=deepseek_llm,
    verbose=True
)

analyst = Agent(
    role="分析师",
    goal="对提炼出的信息进行归纳、分类，并转换为适合可视化的结构化数据",
    backstory="你是一位数据分析师，擅长将非结构化信息转换为结构化数据。",
    tools=[data_structuring_tool],
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
              "6. 考虑用户交互体验和内容可读性",
    tools=[visualization_tool],
    llm=deepseek_llm,
    verbose=True
)

def process_text_with_crewai(text: str) -> Dict[str, Any]:
    """使用 CrewAI 处理文本信息可视化"""

    extraction_task = Task(
        description=f"请分析以下文本内容，提取核心论点、关键数据和重要实体：\n\n{text}",
        agent=researcher,
        expected_output="提取的核心论点、关键数据和重要实体的详细报告"
    )

    structuring_task = Task(
        description="基于研究员提取的信息，进行归纳分类并转换为结构化数据格式（JSON）",
        agent=analyst,
        expected_output="结构化的 JSON 数据，包含实体、指标、分类等信息",
        context=[extraction_task]
    )

    visualization_task = Task(
        description="基于分析师提供的结构化数据，进行深度分析并生成多种类型的可视化展示。\n"
                   "请按以下步骤执行：\n"
                   "1. 分析数据结构，识别关键数据维度和关系\n"
                   "2. 智能选择可视化类型：\n"
                   "   - Card 卡片：适合展示摘要信息、关键数据点、核心论点\n"
                   "   - ECharts 图表：适合展示详细数据分析和趋势\n"
                   "3. 为 Card 卡片生成：标题、摘要、关键数据点、核心洞察\n"
                   "4. 为 ECharts 图表选择最适合的类型（柱状图、折线图、饼图、散点图等）\n"
                   "5. 确保不同可视化类型间有逻辑关联，形成完整的数据分析报告\n",
        agent=visualizer,
        expected_output="包含可视化项的JSON对象：\n"
                       "visualizations: 可视化项数组，每个项包含：\n"
                       "1. Card 卡片配置：\n"
                       "   - type: 'card'\n"
                       "   - card_id: 卡片唯一标识\n"
                       "   - title: 卡片标题\n"
                       "   - summary: 摘要内容\n"
                       "   - key_points: 关键数据点列表\n"
                       "   - insights: 核心洞察\n"
                       "2. ECharts 图表配置：\n"
                       "   - type: 'echarts'\n"
                       "   - chart_id: 图表唯一标识\n"
                       "   - title: 图表标题\n"
                       "   - config: 完整的ECharts配置，不需要包含color相关配置，不允许出现javascript函数\n",
        context=[structuring_task]
    )

    crew = Crew(
        agents=[researcher, analyst, visualizer],
        tasks=[extraction_task, structuring_task, visualization_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    return {
        "extraction_result": str(extraction_task.output) if extraction_task.output else "未完成",
        "structuring_result": str(structuring_task.output) if structuring_task.output else "未完成",
        "visualization_result": str(visualization_task.output) if visualization_task.output else "未完成",
        "final_result": str(result) if result else "未完成"
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

        # 保存结果
        serializable_results = {
            "extraction_result": str(results.get('extraction_result', '')),
            "structuring_result": str(results.get('structuring_result', '')),
            "visualization_result": str(results.get('visualization_result', '')),
            "final_result": str(results.get('final_result', '')),
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

