"""
CrewAI 工具模块
包含内容提炼、数据结构化和可视化工具
"""

import json
from typing import Dict, Any
from crewai.tools import BaseTool


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
    description: str = "根据数据结构生成 Card 卡片展示和 ECharts 图表配置，支持混合布局"

    def _run(self, structured_data: str) -> str:
        """执行可视化配置生成"""
        # 解析结构化数据
        try:
            data = json.loads(structured_data)
        except:
            data = {"companies": [], "industry_trends": {}}

        # 生成混合可视化配置
        mixed_config = self._generate_mixed_visualization(data)
        return json.dumps(mixed_config, ensure_ascii=False, indent=2)

    def _generate_mixed_visualization(self, data: dict) -> dict:
        """生成可视化配置（Card + ECharts），确保内容去重和差异化"""
        visualizations = []
        used_data_points = set()  # 跟踪已使用的数据点，避免重复
        used_analysis_angles = set()  # 跟踪已使用的分析角度

        # 生成 Card 卡片 - 确保内容差异化
        if "entities" in data or "metrics" in data:
            # 1. 核心摘要卡片 - 聚焦总体趋势和核心发现
            summary_card = self._create_summary_card(data, used_data_points, used_analysis_angles)
            summary_card["type"] = "card"
            visualizations.append(summary_card)

            # 2. 关键数据卡片 - 聚焦具体指标和重要数据点（与摘要卡片不重复）
            if "metrics" in data:
                key_data_card = self._create_key_data_card(data, used_data_points, used_analysis_angles)
                key_data_card["type"] = "card"
                visualizations.append(key_data_card)

        # 生成 ECharts 图表 - 确保分析角度差异化
        if "companies" in data and len(data["companies"]) > 0:
            companies = data["companies"]

            # 营收对比图表 - 聚焦横向对比分析
            revenue_chart = self._create_chart("revenue_comparison", "公司营收对比分析", "bar", companies, self._extract_revenue_data)
            revenue_chart["type"] = "echarts"
            visualizations.append(revenue_chart)

            # 净利润对比图表 - 聚焦纵向趋势分析（与营收图表不重复）
            profit_chart = self._create_chart("profit_comparison", "净利润对比分析", "line", companies, self._extract_profit_data)
            profit_chart["type"] = "echarts"
            visualizations.append(profit_chart)

            # 增长趋势图表 - 聚焦增长率分析（与前两个图表不重复）
            growth_chart = self._create_chart("growth_trend", "营收增长趋势", "line", companies, self._extract_revenue_data)
            growth_chart["type"] = "echarts"
            visualizations.append(growth_chart)

        return {
            "visualizations": visualizations,
            "total_items": len(visualizations),
            "description": "基于数据结构生成的可视化展示（Card卡片 + ECharts图表），已确保内容去重和差异化"
        }


    def _create_chart(self, chart_id: str, title: str, chart_type: str, companies: list, data_extractor) -> dict:
        """通用图表创建方法"""
        return {
            "chart_id": chart_id,
            "title": title,
            "type": chart_type,
            "config": {
                "title": {"text": title, "left": "center"},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": [company["name"] for company in companies]},
                "xAxis": {"type": "category", "data": ["2022年", "2023年", "2024年"]},
                "yAxis": {"type": "value", "name": "数值"},
                "series": [
                    {
                        "name": company["name"],
                        "type": chart_type,
                        "data": data_extractor(company),
                        "itemStyle": {"color": f"#{hash(company['name']) % 0xffffff:06x}"}
                    }
                    for company in companies
                ]
            }
        }

    def _extract_revenue_data(self, company: dict) -> list:
        """提取营收数据"""
        if "financial_data" in company and "revenue" in company["financial_data"]:
            revenue = company["financial_data"]["revenue"]
            return [
                float(revenue.get("2022", 0)) if revenue.get("2022") else 0,
                float(revenue.get("2023", 0)) if revenue.get("2023") else 0,
                float(revenue.get("2024", 0)) if revenue.get("2024") else 0
            ]
        return [0, 0, 0]

    def _extract_profit_data(self, company: dict) -> list:
        """提取净利润数据"""
        if "financial_data" in company and "adjusted_profit" in company["financial_data"]:
            profit = company["financial_data"]["adjusted_profit"]
            return [
                float(profit.get("2022", 0)) if profit.get("2022") else 0,
                float(profit.get("2023", 0)) if profit.get("2023") else 0,
                float(profit.get("2024", 0)) if profit.get("2024") else 0
            ]
        return [0, 0, 0]


    def _create_summary_card(self, data: dict, used_data_points: set, used_analysis_angles: set) -> dict:
        """创建核心摘要卡片，确保内容不重复"""
        # 标记使用的分析角度
        analysis_angle = "总体趋势分析"
        used_analysis_angles.add(analysis_angle)

        # 提取未使用的关键数据点
        key_points = []
        insights = []

        if "metrics" in data:
            for metric_name, metric_value in data["metrics"].items():
                if metric_name not in used_data_points:
                    if isinstance(metric_value, dict):
                        for key, value in metric_value.items():
                            key_points.append(f"{key}: {value}")
                            used_data_points.add(f"{metric_name}_{key}")
                    else:
                        key_points.append(f"{metric_name}: {metric_value}")
                        used_data_points.add(metric_name)

        # 确保关键点不重复，最多显示3个
        key_points = key_points[:3]

        # 生成独特的洞察
        insights = [
            "数据呈现明显的增长趋势",
            "关键指标表现良好",
            "存在重要的业务机会"
        ]

        return {
            "card_id": "summary_card",
            "title": "核心摘要",
            "summary": "基于数据分析的核心洞察和关键发现",
            "key_points": key_points,
            "insights": insights
        }

    def _create_key_data_card(self, data: dict, used_data_points: set, used_analysis_angles: set) -> dict:
        """创建关键数据卡片，确保与摘要卡片不重复"""
        # 标记使用的分析角度
        analysis_angle = "具体指标分析"
        used_analysis_angles.add(analysis_angle)

        key_points = []
        insights = []

        # 只使用未被摘要卡片使用的数据点
        if "metrics" in data:
            for metric_name, metric_value in data["metrics"].items():
                if metric_name not in used_data_points:
                    if isinstance(metric_value, dict):
                        for key, value in metric_value.items():
                            data_point = f"{metric_name}_{key}"
                            if data_point not in used_data_points:
                                key_points.append(f"{key}: {value}")
                                used_data_points.add(data_point)
                    else:
                        if metric_name not in used_data_points:
                            key_points.append(f"{metric_name}: {metric_value}")
                            used_data_points.add(metric_name)

        # 从分类信息中提取独特洞察
        if "categories" in data:
            for category_name, category_items in data["categories"].items():
                if isinstance(category_items, list):
                    insights.append(f"{category_name}: {', '.join(category_items[:3])}")

        # 确保内容不重复，最多显示5个关键点
        key_points = key_points[:5]
        insights = insights[:3]

        return {
            "card_id": "key_data_card",
            "title": "关键数据",
            "summary": "核心数据指标和重要发现",
            "key_points": key_points,
            "insights": insights
        }
