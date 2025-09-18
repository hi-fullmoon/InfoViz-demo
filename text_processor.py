"""
文本数据处理模块
用于预处理文本数据，提取结构化信息
"""

import re
import jieba
import pandas as pd
from typing import Dict, List, Any, Tuple
from collections import Counter
from datetime import datetime
import json

class TextProcessor:
    """文本数据处理器"""

    def __init__(self):
        """初始化文本处理器"""
        # 初始化jieba分词
        jieba.initialize()

        # 定义常见的数据模式
        self.patterns = {
            'numbers': r'\d+(?:\.\d+)?',
            'percentages': r'\d+(?:\.\d+)?%',
            'dates': r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            'money': r'[¥$€£]\d+(?:,\d{3})*(?:\.\d{2})?',
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phones': r'\b\d{3,4}[-.]?\d{3,4}[-.]?\d{4}\b',
            'urls': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        }

    def preprocess_text(self, text: str) -> str:
        """
        预处理文本

        Args:
            text: 原始文本

        Returns:
            预处理后的文本
        """
        # 清理文本
        text = re.sub(r'\s+', ' ', text)  # 合并多个空格
        text = text.strip()  # 去除首尾空格

        return text

    def extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取结构化数据

        Args:
            text: 输入文本

        Returns:
            提取的结构化数据
        """
        result = {
            'text_length': len(text),
            'word_count': len(text.split()),
            'char_count': len(text),
            'numbers': [],
            'percentages': [],
            'dates': [],
            'money': [],
            'emails': [],
            'phones': [],
            'urls': [],
            'keywords': [],
            'sentences': []
        }

        # 提取各种模式的数据
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            result[pattern_name] = matches

        # 分词和关键词提取
        words = list(jieba.cut(text))
        # 过滤停用词和短词
        filtered_words = [word for word in words if len(word) > 1 and word not in self._get_stopwords()]
        word_freq = Counter(filtered_words)
        result['keywords'] = word_freq.most_common(20)

        # 句子分割
        sentences = re.split(r'[。！？.!?]', text)
        result['sentences'] = [s.strip() for s in sentences if s.strip()]

        return result

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        提取文本中的实体

        Args:
            text: 输入文本

        Returns:
            实体字典
        """
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'products': [],
            'technologies': []
        }

        # 简单的实体识别规则（可以结合更复杂的NLP模型）
        words = list(jieba.cut(text))

        # 人名识别（简单规则）
        person_patterns = [
            r'[A-Za-z\u4e00-\u9fff]{2,4}先生',
            r'[A-Za-z\u4e00-\u9fff]{2,4}女士',
            r'[A-Za-z\u4e00-\u9fff]{2,4}博士',
            r'[A-Za-z\u4e00-\u9fff]{2,4}教授'
        ]

        for pattern in person_patterns:
            matches = re.findall(pattern, text)
            entities['persons'].extend(matches)

        # 组织名识别
        org_patterns = [
            r'[A-Za-z\u4e00-\u9fff]+公司',
            r'[A-Za-z\u4e00-\u9fff]+集团',
            r'[A-Za-z\u4e00-\u9fff]+大学',
            r'[A-Za-z\u4e00-\u9fff]+研究院',
            r'[A-Za-z\u4e00-\u9fff]+中心'
        ]

        for pattern in org_patterns:
            matches = re.findall(pattern, text)
            entities['organizations'].extend(matches)

        # 地名识别
        location_patterns = [
            r'[A-Za-z\u4e00-\u9fff]+市',
            r'[A-Za-z\u4e00-\u9fff]+省',
            r'[A-Za-z\u4e00-\u9fff]+县',
            r'[A-Za-z\u4e00-\u9fff]+区'
        ]

        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            entities['locations'].extend(matches)

        return entities

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        简单的情感分析

        Args:
            text: 输入文本

        Returns:
            情感分析结果
        """
        # 简单的情感词典
        positive_words = ['好', '优秀', '成功', '增长', '提升', '改善', '满意', '喜欢', '推荐', '积极']
        negative_words = ['差', '失败', '下降', '问题', '困难', '不满', '批评', '负面', '糟糕', '消极']

        words = list(jieba.cut(text))

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            sentiment_score = 0
            sentiment_label = '中性'
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            if sentiment_score > 0.1:
                sentiment_label = '正面'
            elif sentiment_score < -0.1:
                sentiment_label = '负面'
            else:
                sentiment_label = '中性'

        return {
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'total_sentiment_words': total_sentiment_words
        }

    def create_data_summary(self, text: str) -> Dict[str, Any]:
        """
        创建数据摘要

        Args:
            text: 输入文本

        Returns:
            数据摘要
        """
        structured_data = self.extract_structured_data(text)
        entities = self.extract_entities(text)
        sentiment = self.analyze_sentiment(text)

        summary = {
            'basic_stats': {
                'text_length': structured_data['text_length'],
                'word_count': structured_data['word_count'],
                'sentence_count': len(structured_data['sentences']),
                'unique_words': len(set(structured_data['keywords']))
            },
            'data_extraction': {
                'numbers_found': len(structured_data['numbers']),
                'percentages_found': len(structured_data['percentages']),
                'dates_found': len(structured_data['dates']),
                'money_found': len(structured_data['money']),
                'emails_found': len(structured_data['emails']),
                'phones_found': len(structured_data['phones']),
                'urls_found': len(structured_data['urls'])
            },
            'entities': entities,
            'sentiment': sentiment,
            'top_keywords': structured_data['keywords'][:10],
            'extracted_data': structured_data
        }

        return summary

    def _get_stopwords(self) -> set:
        """
        获取停用词列表

        Returns:
            停用词集合
        """
        return {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'
        }
