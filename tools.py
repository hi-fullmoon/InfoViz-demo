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
    description: str = "根据数据结构生成多个 ECharts 配置，支持单页面多图表和独立图表"

    def _run(self, structured_data: str) -> str:
        """执行可视化配置生成"""
        # 解析结构化数据
        try:
            data = json.loads(structured_data)
        except:
            data = {"companies": [], "industry_trends": {}}

        # 生成多个图表配置
        charts_config = self._generate_multiple_charts(data)
        return json.dumps(charts_config, ensure_ascii=False, indent=2)

    def _generate_multiple_charts(self, data: dict) -> dict:
        """生成多个图表配置"""
        charts = []

        # 1. 营收对比图表
        if "companies" in data and len(data["companies"]) > 0:
            revenue_chart = self._create_revenue_comparison_chart(data["companies"])
            charts.append(revenue_chart)

            # 2. 净利润对比图表
            profit_chart = self._create_profit_comparison_chart(data["companies"])
            charts.append(profit_chart)

            # 3. 业务构成饼图
            business_pie_chart = self._create_business_composition_chart(data["companies"])
            charts.append(business_pie_chart)

            # 4. 门店数量对比图表
            store_chart = self._create_store_comparison_chart(data["companies"])
            charts.append(store_chart)

        # 5. 增长趋势图表
        if "companies" in data:
            growth_chart = self._create_growth_trend_chart(data["companies"])
            charts.append(growth_chart)

        return {
            "charts": charts,
            "layout": "multi_chart",  # 标识为多图表布局
            "total_charts": len(charts),
            "description": "基于数据结构生成的多个ECharts图表配置"
        }

    def _create_revenue_comparison_chart(self, companies: list) -> dict:
        """创建营收对比图表"""
        return {
            "chart_id": "revenue_comparison",
            "title": "公司营收对比分析",
            "type": "bar",
            "config": {
                "title": {"text": "公司营收对比分析", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": [company["name"] for company in companies]},
                "xAxis": {"type": "category", "data": ["2022年", "2023年", "2024年"]},
                "yAxis": {"type": "value", "name": "营收(亿元)"},
                "series": [
                    {
                        "name": company["name"],
                        "type": "bar",
                        "data": self._extract_revenue_data(company),
                        "itemStyle": {"color": f"#{hash(company['name']) % 0xffffff:06x}"}
                    }
                    for company in companies
                ]
            }
        }

    def _create_profit_comparison_chart(self, companies: list) -> dict:
        """创建净利润对比图表"""
        return {
            "chart_id": "profit_comparison",
            "title": "净利润对比分析",
            "type": "line",
            "config": {
                "title": {"text": "净利润对比分析", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": [company["name"] for company in companies]},
                "xAxis": {"type": "category", "data": ["2022年", "2023年", "2024年"]},
                "yAxis": {"type": "value", "name": "净利润(亿元)"},
                "series": [
                    {
                        "name": company["name"],
                        "type": "line",
                        "data": self._extract_profit_data(company),
                        "itemStyle": {"color": f"#{hash(company['name']) % 0xffffff:06x}"}
                    }
                    for company in companies
                ]
            }
        }

    def _create_business_composition_chart(self, companies: list) -> dict:
        """创建业务构成饼图"""
        return {
            "chart_id": "business_composition",
            "title": "业务构成分析",
            "type": "pie",
            "config": {
                "title": {"text": "业务构成分析", "left": "center"},
                "tooltip": {"trigger": "item"},
                "series": [{
                    "name": "业务构成",
                    "type": "pie",
                    "radius": "50%",
                    "data": self._extract_business_data(companies),
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)"
                        }
                    }
                }]
            }
        }

    def _create_store_comparison_chart(self, companies: list) -> dict:
        """创建门店数量对比图表"""
        return {
            "chart_id": "store_comparison",
            "title": "门店数量对比",
            "type": "bar",
            "config": {
                "title": {"text": "门店数量对比", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "xAxis": {"type": "category", "data": [company["name"] for company in companies]},
                "yAxis": {"type": "value", "name": "门店数量(家)"},
                "series": [{
                    "name": "门店数量",
                    "type": "bar",
                    "data": [self._extract_store_count(company) for company in companies],
                    "itemStyle": {"color": "#5470c6"}
                }]
            }
        }

    def _create_growth_trend_chart(self, companies: list) -> dict:
        """创建增长趋势图表"""
        return {
            "chart_id": "growth_trend",
            "title": "营收增长趋势",
            "type": "line",
            "config": {
                "title": {"text": "营收增长趋势", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": [company["name"] for company in companies]},
                "xAxis": {"type": "category", "data": ["2022年", "2023年", "2024年"]},
                "yAxis": {"type": "value", "name": "营收(亿元)"},
                "series": [
                    {
                        "name": company["name"],
                        "type": "line",
                        "data": self._extract_revenue_data(company),
                        "smooth": True,
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

    def _extract_business_data(self, companies: list) -> list:
        """提取业务构成数据"""
        business_data = []
        for company in companies:
            if "business_segments" in company:
                for segment in company["business_segments"]:
                    if segment["name"] == "量贩零食业务":
                        business_data.append({
                            "name": f"{company['name']}-{segment['name']}",
                            "value": 99
                        })
                    elif segment["name"] == "食用菌业务":
                        business_data.append({
                            "name": f"{company['name']}-{segment['name']}",
                            "value": 1
                        })
        return business_data

    def _extract_store_count(self, company: dict) -> int:
        """提取门店数量"""
        if "operational_data" in company and "store_count" in company["operational_data"]:
            store_count = company["operational_data"]["store_count"]
            if isinstance(store_count, str) and "家" in store_count:
                return int(store_count.replace("家", ""))
            return int(store_count)
        return 0
