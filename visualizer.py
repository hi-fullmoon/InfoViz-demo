"""
数据可视化模块
用于生成各种类型的图表和可视化内容
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

# 设置中文字体
import matplotlib.font_manager as fm
import warnings

# 查找系统中可用的中文字体
def find_chinese_font():
    """查找系统中可用的中文字体"""
    chinese_fonts = []
    for font in fm.fontManager.ttflist:
        font_name = font.name
        if any(keyword in font_name.lower() for keyword in ['chinese', 'cjk', 'han', 'ping', 'hei', 'song', 'kai', 'ming', 'hiragino', 'stheit']):
            chinese_fonts.append(font_name)

    # 常见的macOS中文字体，按优先级排序
    common_fonts = ['Hiragino Sans', 'STHeiti', 'PingFang SC', 'Arial Unicode MS', 'SimHei', 'Microsoft YaHei']

    for font in common_fonts:
        if font in [f.name for f in fm.fontManager.ttflist]:
            return font

    # 如果没有找到中文字体，返回默认字体
    return 'DejaVu Sans'

# 设置字体
chinese_font = find_chinese_font()
plt.rcParams['font.sans-serif'] = [chinese_font, 'Hiragino Sans GB', 'STHeiti', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 强制设置字体，避免回退到Arial
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*missing from font.*')

print(f"使用中文字体: {chinese_font}")

class DataVisualizer:
    """数据可视化器"""

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

    def create_word_cloud(self, text: str, title: str = "词云图",
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
            colormap='viridis',
            font_path=None,  # 让WordCloud自动选择字体
            prefer_horizontal=0.9,
            relative_scaling=0.5,
            min_font_size=10
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
                                     title: str = "关键词频率", top_n: int = 20) -> str:
        """
        创建关键词频率图表

        Args:
            keywords: 关键词列表 [(word, count), ...]
            title: 图表标题
            top_n: 显示前N个关键词

        Returns:
            保存的文件路径
        """
        # 数据验证和清理
        if not keywords:
            print("警告: 关键词列表为空，跳过关键词频率图表生成")
            return None

        # 过滤掉无效数据
        valid_keywords = []
        for word, count in keywords:
            if word and isinstance(count, (int, float)) and not np.isnan(count) and count > 0:
                valid_keywords.append((word, int(count)))

        if not valid_keywords:
            print("警告: 没有有效的关键词数据，跳过关键词频率图表生成")
            return None

        # 准备数据
        top_keywords = valid_keywords[:top_n]
        words, counts = zip(*top_keywords)

        # 确保counts都是整数
        counts = [int(count) for count in counts]

        # 创建图表
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(words)), counts, color=self.colors['primary'])

        # 设置标签
        plt.yticks(range(len(words)), words)
        plt.xlabel('频率', fontsize=12)
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
                                       title: str = "实体分布") -> str:
        """
        创建实体分布图表

        Args:
            entities: 实体字典
            title: 图表标题

        Returns:
            保存的文件路径
        """
        # 数据验证和清理
        if not entities:
            print("警告: 实体数据为空，跳过实体分布图表生成")
            return None

        # 过滤掉空实体类型
        valid_entities = {}
        for entity_type, entity_list in entities.items():
            if entity_list and len(entity_list) > 0:
                valid_entities[entity_type] = entity_list

        if not valid_entities:
            print("警告: 没有有效的实体数据，跳过实体分布图表生成")
            return None

        # 准备数据
        entity_types = list(valid_entities.keys())
        entity_counts = [len(valid_entities[entity_type]) for entity_type in entity_types]

        # 确保所有计数都是有效的
        entity_counts = [int(count) for count in entity_counts if count > 0]

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
                                      title: str = "情感分析") -> str:
        """
        创建情感分析图表

        Args:
            sentiment_data: 情感分析数据
            title: 图表标题

        Returns:
            保存的文件路径
        """
        # 数据验证和清理
        if not sentiment_data:
            print("警告: 情感分析数据为空，跳过情感分析图表生成")
            return None

        # 获取数据并确保是有效数值
        positive_count = sentiment_data.get('positive_count', 0)
        negative_count = sentiment_data.get('negative_count', 0)
        total_sentiment_words = sentiment_data.get('total_sentiment_words', 0)

        # 处理NaN值
        positive_count = 0 if np.isnan(positive_count) else int(positive_count)
        negative_count = 0 if np.isnan(negative_count) else int(negative_count)
        total_sentiment_words = 0 if np.isnan(total_sentiment_words) else int(total_sentiment_words)

        # 计算中性情感数量
        neutral_count = max(0, total_sentiment_words - positive_count - negative_count)

        # 准备数据
        labels = ['正面', '负面', '中性']
        counts = [positive_count, negative_count, neutral_count]

        # 确保所有计数都是非负数
        counts = [max(0, int(count)) for count in counts]

        # 如果所有计数都为0，跳过图表生成
        if sum(counts) == 0:
            print("警告: 情感分析数据全为0，跳过情感分析图表生成")
            return None

        # 创建子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # 饼图
        colors = [self.colors['success'], self.colors['warning'], self.colors['info']]
        ax1.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('情感分布', fontsize=14, fontweight='bold')

        # 柱状图
        bars = ax2.bar(labels, counts, color=colors)
        ax2.set_title('情感统计', fontsize=14, fontweight='bold')
        ax2.set_ylabel('数量')

        # 添加数值标签
        for bar, count in zip(bars, counts):
            if count > 0:  # 只为非零值添加标签
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
                                     title: str = "数据提取摘要") -> str:
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
        stats_labels = ['文本长度', '词数', '句子数', '唯一词数']
        stats_values = [
            basic_stats.get('text_length', 0),
            basic_stats.get('word_count', 0),
            basic_stats.get('sentence_count', 0),
            basic_stats.get('unique_words', 0)
        ]

        # 处理NaN值并确保是整数
        stats_values = [0 if np.isnan(val) else int(val) for val in stats_values]

        bars1 = ax1.bar(stats_labels, stats_values, color=self.colors['primary'])
        ax1.set_title('基本统计', fontsize=14, fontweight='bold')
        ax1.set_ylabel('数量')

        # 添加数值标签
        max_val = max(stats_values) if stats_values else 1
        for bar, value in zip(bars1, stats_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.01,
                    str(value), ha='center', va='bottom')

        # 数据提取统计
        extraction_labels = ['数字', '百分比', '日期', '金额', '邮箱', '电话', '网址']
        extraction_values = [
            data_extraction.get('numbers_found', 0),
            data_extraction.get('percentages_found', 0),
            data_extraction.get('dates_found', 0),
            data_extraction.get('money_found', 0),
            data_extraction.get('emails_found', 0),
            data_extraction.get('phones_found', 0),
            data_extraction.get('urls_found', 0)
        ]

        # 处理NaN值并确保是整数
        extraction_values = [0 if np.isnan(val) else int(val) for val in extraction_values]

        bars2 = ax2.bar(extraction_labels, extraction_values, color=self.colors['secondary'])
        ax2.set_title('数据提取统计', fontsize=14, fontweight='bold')
        ax2.set_ylabel('数量')
        ax2.tick_params(axis='x', rotation=45)

        # 添加数值标签
        max_val = max(extraction_values) if extraction_values else 1
        for bar, value in zip(bars2, extraction_values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.01,
                    str(value), ha='center', va='bottom')

        # 实体统计
        entities = data_summary.get('entities', {})
        entity_types = list(entities.keys())
        entity_counts = [len(entities[entity_type]) for entity_type in entity_types]

        # 过滤掉空实体类型
        valid_entities = [(entity_type, count) for entity_type, count in zip(entity_types, entity_counts) if count > 0]
        if valid_entities:
            entity_types, entity_counts = zip(*valid_entities)
        else:
            entity_types, entity_counts = [], []

        if entity_types:
            bars3 = ax3.bar(entity_types, entity_counts, color=self.colors['accent'])
            ax3.set_title('实体统计', fontsize=14, fontweight='bold')
            ax3.set_ylabel('数量')

            # 添加数值标签
            max_val = max(entity_counts) if entity_counts else 1
            for bar, count in zip(bars3, entity_counts):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.01,
                        str(count), ha='center', va='bottom')
        else:
            ax3.text(0.5, 0.5, '无实体数据', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('实体统计', fontsize=14, fontweight='bold')

        # 情感分析
        sentiment = data_summary.get('sentiment', {})
        sentiment_labels = ['正面', '负面', '中性']

        positive_count = sentiment.get('positive_count', 0)
        negative_count = sentiment.get('negative_count', 0)
        total_sentiment_words = sentiment.get('total_sentiment_words', 0)

        # 处理NaN值
        positive_count = 0 if np.isnan(positive_count) else int(positive_count)
        negative_count = 0 if np.isnan(negative_count) else int(negative_count)
        total_sentiment_words = 0 if np.isnan(total_sentiment_words) else int(total_sentiment_words)

        neutral_count = max(0, total_sentiment_words - positive_count - negative_count)

        sentiment_values = [positive_count, negative_count, neutral_count]
        sentiment_values = [max(0, int(val)) for val in sentiment_values]

        bars4 = ax4.bar(sentiment_labels, sentiment_values,
                       color=[self.colors['success'], self.colors['warning'], self.colors['info']])
        ax4.set_title('情感分析', fontsize=14, fontweight='bold')
        ax4.set_ylabel('数量')

        # 添加数值标签
        max_val = max(sentiment_values) if sentiment_values else 1
        for bar, value in zip(bars4, sentiment_values):
            if value > 0:
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.01,
                        str(value), ha='center', va='bottom')

        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()

        # 保存图片
        filename = f"data_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        return filepath

    def create_interactive_dashboard(self, data_summary: Dict[str, Any],
                                   title: str = "交互式数据仪表板") -> str:
        """
        创建交互式数据仪表板

        Args:
            data_summary: 数据摘要
            title: 仪表板标题

        Returns:
            保存的HTML文件路径
        """
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('基本统计', '数据提取', '实体分布', '情感分析'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )

        # 基本统计
        basic_stats = data_summary.get('basic_stats', {})
        stats_labels = ['文本长度', '词数', '句子数', '唯一词数']
        stats_values = [
            basic_stats.get('text_length', 0),
            basic_stats.get('word_count', 0),
            basic_stats.get('sentence_count', 0),
            basic_stats.get('unique_words', 0)
        ]

        # 处理NaN值并确保是整数
        stats_values = [0 if np.isnan(val) else int(val) for val in stats_values]

        fig.add_trace(
            go.Bar(x=stats_labels, y=stats_values, name='基本统计',
                  marker_color=self.colors['primary']),
            row=1, col=1
        )

        # 数据提取统计
        data_extraction = data_summary.get('data_extraction', {})
        extraction_labels = ['数字', '百分比', '日期', '金额', '邮箱', '电话', '网址']
        extraction_values = [
            data_extraction.get('numbers_found', 0),
            data_extraction.get('percentages_found', 0),
            data_extraction.get('dates_found', 0),
            data_extraction.get('money_found', 0),
            data_extraction.get('emails_found', 0),
            data_extraction.get('phones_found', 0),
            data_extraction.get('urls_found', 0)
        ]

        # 处理NaN值并确保是整数
        extraction_values = [0 if np.isnan(val) else int(val) for val in extraction_values]

        fig.add_trace(
            go.Bar(x=extraction_labels, y=extraction_values, name='数据提取',
                  marker_color=self.colors['secondary']),
            row=1, col=2
        )

        # 实体分布
        entities = data_summary.get('entities', {})
        entity_types = list(entities.keys())
        entity_counts = [len(entities[entity_type]) for entity_type in entity_types]

        # 过滤掉空实体类型
        valid_entities = [(entity_type, count) for entity_type, count in zip(entity_types, entity_counts) if count > 0]
        if valid_entities:
            entity_types, entity_counts = zip(*valid_entities)
            fig.add_trace(
                go.Pie(labels=entity_types, values=entity_counts, name='实体分布'),
                row=2, col=1
            )
        else:
            # 如果没有实体数据，显示空饼图
            fig.add_trace(
                go.Pie(labels=['无数据'], values=[1], name='实体分布'),
                row=2, col=1
            )

        # 情感分析
        sentiment = data_summary.get('sentiment', {})
        sentiment_labels = ['正面', '负面', '中性']

        positive_count = sentiment.get('positive_count', 0)
        negative_count = sentiment.get('negative_count', 0)
        total_sentiment_words = sentiment.get('total_sentiment_words', 0)

        # 处理NaN值
        positive_count = 0 if np.isnan(positive_count) else int(positive_count)
        negative_count = 0 if np.isnan(negative_count) else int(negative_count)
        total_sentiment_words = 0 if np.isnan(total_sentiment_words) else int(total_sentiment_words)

        neutral_count = max(0, total_sentiment_words - positive_count - negative_count)

        sentiment_values = [positive_count, negative_count, neutral_count]
        sentiment_values = [max(0, int(val)) for val in sentiment_values]

        fig.add_trace(
            go.Bar(x=sentiment_labels, y=sentiment_values, name='情感分析',
                  marker_color=[self.colors['success'], self.colors['warning'], self.colors['info']]),
            row=2, col=2
        )

        # 更新布局
        fig.update_layout(
            title_text=title,
            showlegend=False,
            height=800,
            template='plotly_white'
        )

        # 保存HTML文件
        filename = f"interactive_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.output_dir, filename)
        fig.write_html(filepath)

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
            if text and text.strip():
                try:
                    word_cloud_path = self.create_word_cloud(text)
                    if word_cloud_path:
                        visualizations['word_cloud'] = word_cloud_path
                except Exception as e:
                    print(f"词云图生成失败: {e}")

            # 关键词频率图
            if 'top_keywords' in data_summary and data_summary['top_keywords']:
                try:
                    keyword_path = self.create_keyword_frequency_chart(
                        data_summary['top_keywords']
                    )
                    if keyword_path:
                        visualizations['keyword_frequency'] = keyword_path
                except Exception as e:
                    print(f"关键词频率图生成失败: {e}")

            # 实体分布图
            if 'entities' in data_summary and data_summary['entities']:
                try:
                    entity_path = self.create_entity_distribution_chart(
                        data_summary['entities']
                    )
                    if entity_path:
                        visualizations['entity_distribution'] = entity_path
                except Exception as e:
                    print(f"实体分布图生成失败: {e}")

            # 情感分析图
            if 'sentiment' in data_summary and data_summary['sentiment']:
                try:
                    sentiment_path = self.create_sentiment_analysis_chart(
                        data_summary['sentiment']
                    )
                    if sentiment_path:
                        visualizations['sentiment_analysis'] = sentiment_path
                except Exception as e:
                    print(f"情感分析图生成失败: {e}")

            # 数据摘要图
            try:
                summary_path = self.create_data_extraction_summary(data_summary)
                if summary_path:
                    visualizations['data_summary'] = summary_path
            except Exception as e:
                print(f"数据摘要图生成失败: {e}")

            # 交互式仪表板
            try:
                dashboard_path = self.create_interactive_dashboard(data_summary)
                if dashboard_path:
                    visualizations['interactive_dashboard'] = dashboard_path
            except Exception as e:
                print(f"交互式仪表板生成失败: {e}")

        except Exception as e:
            print(f"可视化生成过程中出现错误: {e}")

        return visualizations
