"""
DeepSeek API客户端模块
用于调用DeepSeek模型进行文本分析和数据提取
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DeepSeekClient:
    """DeepSeek API客户端"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化DeepSeek客户端

        Args:
            api_key: DeepSeek API密钥，如果不提供则从环境变量获取
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("请设置DEEPSEEK_API_KEY环境变量或直接传入api_key参数")

        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def extract_data_from_text(self, text: str, extraction_type: str = "comprehensive") -> Dict[str, Any]:
        """
        从文本中提取数据和重要信息

        Args:
            text: 要分析的文本
            extraction_type: 提取类型 ("comprehensive", "entities", "sentiment", "keywords")

        Returns:
            提取的数据字典
        """
        prompts = {
            "comprehensive": """
            请分析以下文本，提取以下信息并以JSON格式返回：
            1. 关键实体（人物、地点、组织、产品等）
            2. 重要数字和统计数据
            3. 时间信息
            4. 情感倾向（正面/负面/中性）
            5. 主要主题和关键词
            6. 重要事件或趋势
            7. 可量化的指标

            请确保返回的数据结构清晰，便于后续可视化处理。

            文本内容：
            """,
            "entities": """
            请从以下文本中提取所有重要实体，包括：
            - 人名
            - 地名
            - 组织名
            - 产品名
            - 其他重要名词

            以JSON格式返回，包含实体类型和实体名称。

            文本内容：
            """,
            "sentiment": """
            请分析以下文本的情感倾向，包括：
            - 整体情感（正面/负面/中性）
            - 情感强度（1-10分）
            - 关键情感词汇
            - 情感变化趋势

            以JSON格式返回分析结果。

            文本内容：
            """,
            "keywords": """
            请从以下文本中提取关键词，包括：
            - 高频词汇
            - 重要概念
            - 专业术语
            - 主题词

            以JSON格式返回，包含词汇和频率。

            文本内容：
            """
        }

        prompt = prompts.get(extraction_type, prompts["comprehensive"]) + text

        try:
            response = self._make_request(prompt)
            return self._parse_response(response)
        except Exception as e:
            print(f"数据提取失败: {e}")
            return {"error": str(e)}

    def generate_visualization_suggestions(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        基于提取的数据生成可视化建议

        Args:
            extracted_data: 提取的数据

        Returns:
            可视化建议列表
        """
        prompt = f"""
        基于以下提取的数据，请建议最适合的可视化图表类型和配置：

        数据内容：
        {json.dumps(extracted_data, ensure_ascii=False, indent=2)}

        请为每种数据类型推荐：
        1. 图表类型（柱状图、折线图、饼图、散点图、词云等）
        2. 图表配置参数
        3. 数据映射方式
        4. 颜色方案建议
        5. 交互功能建议

        以JSON格式返回建议列表。
        """

        try:
            response = self._make_request(prompt)
            return self._parse_response(response)
        except Exception as e:
            print(f"可视化建议生成失败: {e}")
            return [{"error": str(e)}]

    def _make_request(self, prompt: str) -> Dict[str, Any]:
        """
        向DeepSeek API发送请求

        Args:
            prompt: 提示词

        Returns:
            API响应
        """
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 4000
        }

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")

        return response.json()

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析API响应

        Args:
            response: API响应

        Returns:
            解析后的数据
        """
        try:
            content = response['choices'][0]['message']['content']
            # 尝试解析JSON
            if content.strip().startswith('{') or content.strip().startswith('['):
                return json.loads(content)
            else:
                # 如果不是JSON格式，返回原始内容
                return {"content": content}
        except (KeyError, json.JSONDecodeError) as e:
            return {"error": f"响应解析失败: {e}", "raw_response": response}
