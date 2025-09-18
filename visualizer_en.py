"""
英文版数据可视化模块
避免中文字体显示问题
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import jieba
from typing import Dict, List, Any, Optional, Tuple
import os
from datetime import datetime

# 设置字体为英文
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class DataVisualizerEN:
    """英文版数据可视化器"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化可视化器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 设置颜色主题
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'info': '#6A994E',
            'warning': '#F77F00',
            'light': '#F8F9FA',
            'dark': '#212529'
        }

        # 设置seaborn样式
        sns.set_style("whitegrid")
        sns.set_palette("husl")

    def create_word_cloud(self, text: str, title: str = "Word Cloud",
                         width: int = 800, height: int = 400) -> str:
        """
        创建词云图

        Args:
            text: 文本内容
            title: 图表标题
            width: 图片宽度
            height: 图片高度

        Returns:
            保存的文件路径
        """
        # 分词
        words = jieba.cut(text)
        word_list = [word for word in words if len(word) > 1]
        word_text = ' '.join(word_list)

        # 创建词云
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(word_text)

        # 绘制词云
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, fontweight='bold')

        # 保存图片
        filename = f"wordcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return filepath

    def create_keyword_frequency_chart(self, keywords: List[Tuple[str, int]],
                                     title: str = "Keyword Frequency", top_n: int = 20) -> str:
        """
        创建关键词频率图表

        Args:
            keywords: 关键词列表 [(word, count), ...]
            title: 图表标题
            top_n: 显示前N个关键词

        Returns:
            保存的文件路径
        """
        # 准备数据
        top_keywords = keywords[:top_n]
        words, counts = zip(*top_keywords)

        # 创建图表
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(words)), counts, color=self.colors['primary'])

        # 设置标签
        plt.yticks(range(len(words)), words)
        plt.xlabel('Frequency', fontsize=12)
        plt.title(title, fontsize=16, fontweight='bold')

        # 添加数值标签
        for i, (bar, count) in enumerate(zip(bars, counts)):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontsize=10)

        plt.tight_layout()

        # 保存图片
        filename = f"keyword_frequency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return filepath

    def create_entity_distribution_chart(self, entities: Dict[str, List[str]],
                                       title: str = "Entity Distribution") -> str:
        """
        创建实体分布图表

        Args:
            entities: 实体字典
            title: 图表标题

        Returns:
            保存的文件路径
        """
        # 准备数据
        entity_types = list(entities.keys())
        entity_counts = [len(entities[entity_type]) for entity_type in entity_types]

        # 创建饼图
        plt.figure(figsize=(10, 8))
        colors = [self.colors['primary'], self.colors['secondary'],
                 self.colors['accent'], self.colors['success'], self.colors['info']]

        wedges, texts, autotexts = plt.pie(entity_counts, labels=entity_types,
                                          autopct='%1.1f%%', colors=colors[:len(entity_types)],
                                          startangle=90)

        plt.title(title, fontsize=16, fontweight='bold')

        # 保存图片
        filename = f"entity_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return filepath

    def create_sentiment_analysis_chart(self, sentiment_data: Dict[str, Any],
                                      title: str = "Sentiment Analysis") -> str:
        """
        创建情感分析图表

        Args:
            sentiment_data: 情感分析数据
            title: 图表标题

        Returns:
            保存的文件路径
        """
        # 准备数据
        labels = ['Positive', 'Negative', 'Neutral']
        counts = [
            sentiment_data.get('positive_count', 0),
            sentiment_data.get('negative_count', 0),
            sentiment_data.get('total_sentiment_words', 0) -
            sentiment_data.get('positive_count', 0) -
            sentiment_data.get('negative_count', 0)
        ]

        # 创建子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # 饼图
        colors = [self.colors['success'], self.colors['warning'], self.colors['info']]
        ax1.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')

        # 柱状图
        bars = ax2.bar(labels, counts, color=colors)
        ax2.set_title('Sentiment Statistics', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Count')

        # 添加数值标签
        for bar, count in zip(bars, counts):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')

        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()

        # 保存图片
        filename = f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return filepath

    def create_data_extraction_summary(self, data_summary: Dict[str, Any],
                                     title: str = "Data Extraction Summary") -> str:
        """
        创建数据提取摘要图表

        Args:
            data_summary: 数据摘要
            title: 图表标题

        Returns:
            保存的文件路径
        """
        # 准备数据
        basic_stats = data_summary.get('basic_stats', {})
        data_extraction = data_summary.get('data_extraction', {})

        # 创建子图
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

        # 基本统计
        stats_labels = ['Text Length', 'Word Count', 'Sentence Count', 'Unique Words']
        stats_values = [
            basic_stats.get('text_length', 0),
            basic_stats.get('word_count', 0),
            basic_stats.get('sentence_count', 0),
            basic_stats.get('unique_words', 0)
        ]

        bars1 = ax1.bar(stats_labels, stats_values, color=self.colors['primary'])
        ax1.set_title('Basic Statistics', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Count')

        # 添加数值标签
        for bar, value in zip(bars1, stats_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(stats_values)*0.01,
                    str(value), ha='center', va='bottom')

        # 数据提取统计
        extraction_labels = ['Numbers', 'Percentages', 'Dates', 'Money', 'Emails', 'Phones', 'URLs']
        extraction_values = [
            data_extraction.get('numbers_found', 0),
            data_extraction.get('percentages_found', 0),
            data_extraction.get('dates_found', 0),
            data_extraction.get('money_found', 0),
            data_extraction.get('emails_found', 0),
            data_extraction.get('phones_found', 0),
            data_extraction.get('urls_found', 0)
        ]

        bars2 = ax2.bar(extraction_labels, extraction_values, color=self.colors['secondary'])
        ax2.set_title('Data Extraction Statistics', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Count')
        ax2.tick_params(axis='x', rotation=45)

        # 添加数值标签
        for bar, value in zip(bars2, extraction_values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(extraction_values)*0.01,
                    str(value), ha='center', va='bottom')

        # 实体统计
        entities = data_summary.get('entities', {})
        entity_types = list(entities.keys())
        entity_counts = [len(entities[entity_type]) for entity_type in entity_types]

        bars3 = ax3.bar(entity_types, entity_counts, color=self.colors['accent'])
        ax3.set_title('Entity Statistics', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Count')

        # 添加数值标签
        for bar, count in zip(bars3, entity_counts):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(entity_counts)*0.01,
                    str(count), ha='center', va='bottom')

        # 情感分析
        sentiment = data_summary.get('sentiment', {})
        sentiment_labels = ['Positive', 'Negative', 'Neutral']
        sentiment_values = [
            sentiment.get('positive_count', 0),
            sentiment.get('negative_count', 0),
            sentiment.get('total_sentiment_words', 0) -
            sentiment.get('positive_count', 0) -
            sentiment.get('negative_count', 0)
        ]

        bars4 = ax4.bar(sentiment_labels, sentiment_values,
                       color=[self.colors['success'], self.colors['warning'], self.colors['info']])
        ax4.set_title('Sentiment Analysis', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Count')

        # 添加数值标签
        for bar, value in zip(bars4, sentiment_values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sentiment_values)*0.01,
                    str(value), ha='center', va='bottom')

        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()

        # 保存图片
        filename = f"data_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return filepath

    def generate_all_visualizations(self, data_summary: Dict[str, Any],
                                  text: str = "") -> Dict[str, str]:
        """
        生成所有可视化图表

        Args:
            data_summary: 数据摘要
            text: 原始文本（用于词云）

        Returns:
            生成的文件路径字典
        """
        visualizations = {}

        try:
            # 词云图
            if text:
                visualizations['word_cloud'] = self.create_word_cloud(text)

            # 关键词频率图
            if 'top_keywords' in data_summary:
                visualizations['keyword_frequency'] = self.create_keyword_frequency_chart(
                    data_summary['top_keywords']
                )

            # 实体分布图
            if 'entities' in data_summary:
                visualizations['entity_distribution'] = self.create_entity_distribution_chart(
                    data_summary['entities']
                )

            # 情感分析图
            if 'sentiment' in data_summary:
                visualizations['sentiment_analysis'] = self.create_sentiment_analysis_chart(
                    data_summary['sentiment']
                )

            # 数据摘要图
            visualizations['data_summary'] = self.create_data_extraction_summary(data_summary)

        except Exception as e:
            print(f"可视化生成过程中出现错误: {e}")

        return visualizations
