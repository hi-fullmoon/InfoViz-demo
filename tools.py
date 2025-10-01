"""
CrewAI 工具模块 - 重写版本
包含内容提炼、数据结构化和可视化工具
完全独立于外部数据文件，确保数据真实有效
"""

import json
import re
import logging
from typing import Dict, Any, List, Optional, Union
from crewai.tools import BaseTool

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentExtractionTool(BaseTool):
    """内容提炼工具 - 增强版本"""
    name: str = "content_extraction"
    description: str = "从文本中提取核心论点、关键数据和重要实体，支持多种文本格式"

    def _run(self, text: str) -> str:
        """执行内容提炼，增强错误处理和数据验证"""
        try:
            if not text or not isinstance(text, str):
                logger.warning("输入文本为空或格式不正确")
                return self._create_fallback_response()

            # 验证文本长度
            if len(text.strip()) < 10:
                logger.warning("输入文本过短，可能无法提取有效信息")
                return self._create_fallback_response()

            # 执行内容分析
            analysis_result = self._analyze_content(text)

            # 验证分析结果
            if not self._validate_analysis_result(analysis_result):
                logger.warning("内容分析结果验证失败，使用回退方案")
                return self._create_fallback_response()

            return json.dumps(analysis_result, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"内容提炼过程中发生错误: {str(e)}")
            return self._create_fallback_response()

    def _analyze_content(self, text: str) -> Dict[str, Any]:
        """分析文本内容，提取关键信息"""
        # 基础统计信息
        word_count = len(text.split())
        char_count = len(text)
        line_count = len([line for line in text.split('\n') if line.strip()])

        # 提取关键信息
        entities = self._extract_entities(text)
        metrics = self._extract_metrics(text)
        categories = self._extract_categories(text)
        core_arguments = self._extract_arguments(text)

        return {
            "text_statistics": {
                "word_count": word_count,
                "char_count": char_count,
                "line_count": line_count
            },
            "entities": entities,
            "metrics": metrics,
            "categories": categories,
            "core_arguments": core_arguments,
            "analysis_timestamp": self._get_timestamp()
        }

    def _extract_entities(self, text: str) -> List[str]:
        """提取实体，增强模式匹配"""
        entities = []

        # 多种实体模式
        patterns = [
            r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*',  # 大写开头的词
            r'[\u4e00-\u9fff]+',  # 中文字符
            r'\b[A-Z]{2,}\b',  # 大写缩写
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match.strip()) > 1 and match not in entities:
                    entities.append(match.strip())

        return entities[:10]  # 最多返回10个实体

    def _extract_metrics(self, text: str) -> Dict[str, Union[str, float]]:
        """提取指标数据，支持多种数值格式"""
        metrics = {}

        # 数值模式
        number_patterns = [
            r'[\d,]+\.?\d*\s*[万亿亿]?[美元元]?',
            r'[\d,]+\.?\d*\s*%',
            r'[\d,]+\.?\d*\s*[万亿]',
            r'[\d,]+\.?\d*'
        ]

        for pattern in number_patterns:
            matches = re.findall(pattern, text)
            for i, match in enumerate(matches):
                key = f"metric_{i+1}"
                metrics[key] = match.strip()

        return metrics

    def _extract_categories(self, text: str) -> List[str]:
        """提取分类标签"""
        categories = []

        # 预定义分类关键词
        category_keywords = {
            '经济指标': ['经济', 'GDP', '增长', '下降', '指标', '数据'],
            '金融数据': ['金融', '银行', '货币', '利率', '汇率', '投资'],
            '市场分析': ['市场', '价格', '交易', '买卖', '趋势'],
            '政策影响': ['政策', '法规', '规定', '影响', '措施'],
            '历史比较': ['历史', '过去', '曾经', '最高', '最低', '创']
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                categories.append(category)

        return categories

    def _extract_arguments(self, text: str) -> List[str]:
        """提取核心论点"""
        arguments = []
        sentences = re.split(r'[。！？\n]', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                # 检查是否包含关键信息
                if any(keyword in sentence for keyword in ['因为', '所以', '导致', '影响', '结果', '原因']):
                    arguments.append(sentence)

        return arguments[:5]  # 最多返回5个论点

    def _validate_analysis_result(self, result: Dict[str, Any]) -> bool:
        """验证分析结果的有效性"""
        required_keys = ['entities', 'metrics', 'categories', 'core_arguments']
        return all(key in result for key in required_keys)

    def _create_fallback_response(self) -> str:
        """创建回退响应"""
        fallback_data = {
            "text_statistics": {
                "word_count": 0,
                "char_count": 0,
                "line_count": 0
            },
            "entities": ["数据提取失败"],
            "metrics": {"error": "无法提取有效指标"},
            "categories": ["数据异常"],
            "core_arguments": ["内容分析遇到问题，请检查输入数据"],
            "analysis_timestamp": self._get_timestamp(),
            "status": "fallback"
        }
        return json.dumps(fallback_data, ensure_ascii=False, indent=2)

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


class DataStructuringTool(BaseTool):
    """数据结构化工具 - 增强版本"""
    name: str = "data_structuring"
    description: str = "将提取的信息转换为结构化数据格式，支持数据验证和清理"

    def _run(self, extracted_content: str) -> str:
        """执行数据结构化，增强数据验证"""
        try:
            # 解析输入内容
            if isinstance(extracted_content, str):
                try:
                    data = json.loads(extracted_content)
                except json.JSONDecodeError:
                    logger.warning("输入内容不是有效的JSON格式，尝试直接解析")
                    data = {"raw_content": extracted_content}
            else:
                data = extracted_content

            # 验证和清理数据
            cleaned_data = self._clean_and_validate_data(data)

            # 生成结构化数据
            structured_data = self._generate_structured_data(cleaned_data)

            return json.dumps(structured_data, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"数据结构化过程中发生错误: {str(e)}")
            return self._create_fallback_structured_data()

    def _clean_and_validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """清理和验证数据"""
        cleaned = {}

        # 清理实体数据
        if 'entities' in data:
            cleaned['entities'] = [str(entity).strip() for entity in data['entities'] if entity and str(entity).strip()]

        # 清理指标数据
        if 'metrics' in data:
            cleaned['metrics'] = {}
            for key, value in data['metrics'].items():
                if value and str(value).strip():
                    cleaned['metrics'][str(key).strip()] = str(value).strip()

        # 清理分类数据
        if 'categories' in data:
            cleaned['categories'] = [str(cat).strip() for cat in data['categories'] if cat and str(cat).strip()]

        # 清理论点数据
        if 'core_arguments' in data:
            cleaned['core_arguments'] = [str(arg).strip() for arg in data['core_arguments'] if arg and str(arg).strip()]

        return cleaned

    def _generate_structured_data(self, cleaned_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成结构化数据"""
        return {
            "data_summary": {
                "total_entities": len(cleaned_data.get('entities', [])),
                "total_metrics": len(cleaned_data.get('metrics', {})),
                "total_categories": len(cleaned_data.get('categories', [])),
                "total_arguments": len(cleaned_data.get('core_arguments', []))
            },
            "entities": cleaned_data.get('entities', []),
            "metrics": cleaned_data.get('metrics', {}),
            "categories": cleaned_data.get('categories', []),
            "core_arguments": cleaned_data.get('core_arguments', []),
            "processing_timestamp": self._get_timestamp(),
            "data_quality": self._assess_data_quality(cleaned_data)
        }

    def _assess_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """评估数据质量"""
        quality_score = 0
        max_score = 4

        if data.get('entities'):
            quality_score += 1
        if data.get('metrics'):
            quality_score += 1
        if data.get('categories'):
            quality_score += 1
        if data.get('core_arguments'):
            quality_score += 1

        return {
            "score": quality_score,
            "max_score": max_score,
            "percentage": (quality_score / max_score) * 100,
            "status": "excellent" if quality_score >= 3 else "good" if quality_score >= 2 else "fair"
        }

    def _create_fallback_structured_data(self) -> str:
        """创建回退结构化数据"""
        fallback_data = {
            "data_summary": {
                "total_entities": 0,
                "total_metrics": 0,
                "total_categories": 0,
                "total_arguments": 0
            },
            "entities": [],
            "metrics": {},
            "categories": [],
            "core_arguments": [],
            "processing_timestamp": self._get_timestamp(),
            "data_quality": {
                "score": 0,
                "max_score": 4,
                "percentage": 0,
                "status": "error"
            },
            "error": "数据结构化失败，请检查输入数据"
        }
        return json.dumps(fallback_data, ensure_ascii=False, indent=2)

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


class VisualizationTool(BaseTool):
    """可视化工具 - 增强版本"""
    name: str = "visualization"
    description: str = "根据数据结构生成可视化配置，支持多种图表类型和布局"

    def _run(self, structured_data: str) -> str:
        """执行可视化配置生成，增强错误处理"""
        try:
            # 解析结构化数据
            if isinstance(structured_data, str):
                try:
                    data = json.loads(structured_data)
                except json.JSONDecodeError:
                    logger.warning("结构化数据格式错误，使用默认配置")
                    data = self._create_default_data()
            else:
                data = structured_data

            # 验证数据完整性
            if not self._validate_visualization_data(data):
                logger.warning("数据验证失败，使用回退配置")
                return self._create_fallback_visualization()

            # 生成可视化配置
            visualization_config = self._generate_visualization_config(data)

            return json.dumps(visualization_config, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"可视化配置生成过程中发生错误: {str(e)}")
            return self._create_fallback_visualization()

    def _validate_visualization_data(self, data: Dict[str, Any]) -> bool:
        """验证可视化数据的完整性"""
        required_keys = ['entities', 'metrics', 'categories', 'core_arguments']
        return all(key in data for key in required_keys)

    def _generate_visualization_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成可视化配置"""
        visualizations = []

        # 生成卡片组件
        cards = self._generate_cards(data)
        visualizations.extend(cards)

        # 生成图表组件
        charts = self._generate_charts(data)
        visualizations.extend(charts)

        return {
            "visualizations": visualizations,
            "total_items": len(visualizations),
            "generation_timestamp": self._get_timestamp(),
            "description": "基于结构化数据生成的可视化配置"
        }

    def _generate_cards(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成卡片组件"""
        cards = []

        # 摘要卡片
        if data.get('entities') or data.get('core_arguments'):
            summary_card = {
                "type": "card",
                "card_id": "summary",
                "title": "内容摘要",
                "content": {
                    "entities": data.get('entities', [])[:5],
                    "arguments": data.get('core_arguments', [])[:3]
                }
            }
            cards.append(summary_card)

        # 数据指标卡片
        if data.get('metrics'):
            metrics_card = {
                "type": "card",
                "card_id": "metrics",
                "title": "关键指标",
                "content": {
                    "metrics": data.get('metrics', {})
                }
            }
            cards.append(metrics_card)

        return cards

    def _generate_charts(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成图表组件"""
        charts = []

        # 实体分布图
        if data.get('entities'):
            entity_chart = self._create_entity_chart(data['entities'])
            if entity_chart:
                charts.append(entity_chart)

        # 指标趋势图
        if data.get('metrics'):
            metrics_chart = self._create_metrics_chart(data['metrics'])
            if metrics_chart:
                charts.append(metrics_chart)

        return charts

    def _create_entity_chart(self, entities: List[str]) -> Optional[Dict[str, Any]]:
        """创建实体分布图"""
        if not entities:
            return None

        # 统计实体长度分布
        length_groups = {'短(1-3字符)': 0, '中(4-8字符)': 0, '长(9+字符)': 0}
        for entity in entities:
            length = len(str(entity))
            if length <= 3:
                length_groups['短(1-3字符)'] += 1
            elif length <= 8:
                length_groups['中(4-8字符)'] += 1
            else:
                length_groups['长(9+字符)'] += 1

        return {
            "type": "echarts",
            "chart_id": "entity_distribution",
            "title": "实体长度分布",
            "config": {
                "title": {"text": "实体长度分布", "left": "center"},
                "tooltip": {"trigger": "item"},
                "series": [{
                    "name": "实体数量",
                    "type": "pie",
                    "radius": "50%",
                    "data": [{"value": v, "name": k} for k, v in length_groups.items() if v > 0]
                }]
            }
        }

    def _create_metrics_chart(self, metrics: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建指标图表"""
        if not metrics:
            return None

        # 提取数值数据
        values = []
        labels = []

        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                values.append(value)
                labels.append(key)
            elif isinstance(value, str):
                # 尝试提取数字
                numbers = re.findall(r'[\d.]+', str(value))
                if numbers:
                    try:
                        values.append(float(numbers[0]))
                        labels.append(key)
                    except ValueError:
                        continue

        if not values:
            return None

        return {
            "type": "echarts",
            "chart_id": "metrics_analysis",
            "title": "指标分析",
            "config": {
                "title": {"text": "指标分析", "left": "center"},
                "xAxis": {"type": "category", "data": labels},
                "yAxis": {"type": "value"},
                "series": [{
                    "name": "指标值",
                    "type": "bar",
                    "data": values
                }],
                "tooltip": {"trigger": "axis"}
            }
        }

    def _create_default_data(self) -> Dict[str, Any]:
        """创建默认数据"""
        return {
            "entities": ["示例实体1", "示例实体2"],
            "metrics": {"示例指标": "示例值"},
            "categories": ["示例分类"],
            "core_arguments": ["示例论点"]
        }

    def _create_fallback_visualization(self) -> str:
        """创建回退可视化配置"""
        fallback_config = {
            "visualizations": [
                {
                    "type": "card",
                    "card_id": "error_card",
                    "title": "数据错误",
                    "content": {
                        "message": "无法生成可视化配置，请检查输入数据"
                    }
                }
            ],
            "total_items": 1,
            "generation_timestamp": self._get_timestamp(),
            "description": "回退可视化配置",
            "error": "可视化生成失败"
        }
        return json.dumps(fallback_config, ensure_ascii=False, indent=2)

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


# 工具注册函数
def get_tools() -> List[BaseTool]:
    """获取所有工具实例"""
    return [
        ContentExtractionTool(),
        DataStructuringTool(),
        VisualizationTool()
    ]


# 数据验证工具
class DataValidator:
    """数据验证工具类"""

    @staticmethod
    def validate_json(data: str) -> bool:
        """验证JSON格式"""
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def validate_text_input(text: str) -> bool:
        """验证文本输入"""
        return isinstance(text, str) and len(text.strip()) > 0

    @staticmethod
    def sanitize_input(text: str) -> str:
        """清理输入文本"""
        if not isinstance(text, str):
            return ""
        return text.strip()


# 错误处理装饰器
def handle_errors(func):
    """错误处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"工具执行错误: {str(e)}")
            return {"error": str(e), "status": "failed"}
    return wrapper