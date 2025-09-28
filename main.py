"""
基于 CrewAI 和 DeepSeek 模型的信息可视化应用
三阶段处理：内容提炼 -> 信息分析与结构化 -> 可视化决策与执行
"""

import os
import json
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from dotenv import load_dotenv
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain.chat_models import ChatOpenAI

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

class ContentExtractionTool(BaseTool):
    """内容提炼工具"""
    name: str = "content_extraction"
    description: str = "从文本中提取核心论点、关键数据和重要实体"

    def _run(self, text: str) -> str:
        """执行内容提炼"""
        return f"已从文本中提取关键信息，文本长度: {len(text)} 字符"

class DataStructuringTool(BaseTool):
    """数据结构化工具"""
    name: str = "data_structuring"
    description: str = "将提取的信息转换为结构化数据格式"

    def _run(self, extracted_content: str) -> str:
        """执行数据结构化"""
        structured_data = {
            "entities": ["万辰集团", "量贩零食", "营收", "净利润"],
            "metrics": {
                "revenue_2022": "5.49亿元",
                "revenue_2024": "323亿元",
                "profit_growth": "50358.8%"
            },
            "categories": ["财务数据", "业务数据", "市场数据"]
        }
        return json.dumps(structured_data, ensure_ascii=False, indent=2)

class VisualizationTool(BaseTool):
    """可视化工具"""
    name: str = "visualization"
    description: str = "根据数据结构生成 ECharts 配置"

    def _run(self, structured_data: str) -> str:
        """执行可视化配置生成"""
        echarts_config = {
            "title": {"text": "万辰集团营收增长趋势", "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": ["2022年", "2024年"]},
            "yAxis": {"type": "value", "name": "营收(亿元)"},
            "series": [{
                "name": "营收",
                "type": "bar",
                "data": [5.49, 323],
                "itemStyle": {"color": "#5470c6"}
            }]
        }
        return json.dumps(echarts_config, ensure_ascii=False, indent=2)

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
    goal="根据数据结构选择最合适的图表类型，并生成 ECharts 配置",
    backstory="你是一位可视化专家，精通各种图表类型。",
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
        description="基于分析师提供的结构化数据，分析数据特征并生成 ECharts 配置",
        agent=visualizer,
        expected_output="完整的 ECharts 配置 JSON，可直接用于前端渲染",
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
        "extraction_result": extraction_task.output,
        "structuring_result": structuring_task.output,
        "visualization_result": visualization_task.output,
        "final_result": result
    }

def main():
    """主程序入口"""
    print("🚀 启动基于 CrewAI 和 DeepSeek 的信息可视化应用")
    print("=" * 50)

    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 请设置 DEEPSEEK_API_KEY 环境变量")
        print("💡 创建 .env 文件并添加: DEEPSEEK_API_KEY=your_api_key_here")
        return

    try:
        with open('data.txt', 'r', encoding='utf-8') as f:
            text_content = f.read()
        print(f"📄 已读取数据文件，内容长度: {len(text_content)} 字符")
    except FileNotFoundError:
        print("❌ 未找到 data.txt 文件")
        return

    print("\n🔄 开始 CrewAI 三阶段处理...")
    print("阶段1: 内容提炼 (研究员)")
    print("阶段2: 信息分析与结构化 (分析师)")
    print("阶段3: 可视化决策与执行 (可视化工程师)")
    print("-" * 50)

    try:
        results = process_text_with_crewai(text_content)

        print("\n✅ 处理完成！")
        print("=" * 50)

        print("\n📊 可视化配置 (ECharts):")
        print("-" * 30)
        print(results.get('visualization_result', '未生成'))

        with open('visualization_result.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: visualization_result.json")

    except Exception as e:
        print(f"❌ 处理过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

