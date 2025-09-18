"""
主程序入口
整合DeepSeek API调用、文本处理和数据可视化功能
"""

import os
import json
import argparse
from typing import Dict, Any, Optional
from datetime import datetime

from deepseek_client import DeepSeekClient
from text_processor import TextProcessor
from visualizer import DataVisualizer

class InfoVizDemo:
    """信息可视化演示主类"""

    def __init__(self, api_key: Optional[str] = None, output_dir: str = "output"):
        """
        初始化信息可视化演示

        Args:
            api_key: DeepSeek API密钥
            output_dir: 输出目录
        """
        self.deepseek_client = DeepSeekClient(api_key)
        self.text_processor = TextProcessor()
        self.visualizer = DataVisualizer(output_dir)
        self.output_dir = output_dir

    def process_text(self, text: str, use_deepseek: bool = True,
                    extraction_type: str = "comprehensive") -> Dict[str, Any]:
        """
        处理文本并生成可视化

        Args:
            text: 输入文本
            use_deepseek: 是否使用DeepSeek API
            extraction_type: 提取类型

        Returns:
            处理结果
        """
        print("开始处理文本...")

        # 本地文本处理
        print("1. 执行本地文本分析...")
        local_summary = self.text_processor.create_data_summary(text)

        result = {
            'input_text': text,
            'local_analysis': local_summary,
            'deepseek_analysis': None,
            'visualizations': {},
            'processing_time': datetime.now().isoformat()
        }

        # DeepSeek API分析
        if use_deepseek:
            try:
                print("2. 调用DeepSeek API进行深度分析...")
                deepseek_data = self.deepseek_client.extract_data_from_text(text, extraction_type)
                result['deepseek_analysis'] = deepseek_data

                # 生成可视化建议
                print("3. 生成可视化建议...")
                viz_suggestions = self.deepseek_client.generate_visualization_suggestions(deepseek_data)
                result['visualization_suggestions'] = viz_suggestions

            except Exception as e:
                print(f"DeepSeek API调用失败: {e}")
                result['deepseek_error'] = str(e)

        # 生成可视化图表
        print("4. 生成可视化图表...")
        try:
            visualizations = self.visualizer.generate_all_visualizations(
                local_summary, text
            )
            result['visualizations'] = visualizations
            print(f"生成了 {len(visualizations)} 个可视化图表")
        except Exception as e:
            print(f"可视化生成失败: {e}")
            result['visualization_error'] = str(e)

        # 保存结果
        print("5. 保存分析结果...")
        self._save_results(result)

        return result

    def process_file(self, file_path: str, use_deepseek: bool = True,
                    extraction_type: str = "comprehensive") -> Dict[str, Any]:
        """
        处理文件中的文本

        Args:
            file_path: 文件路径
            use_deepseek: 是否使用DeepSeek API
            extraction_type: 提取类型

        Returns:
            处理结果
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            print(f"成功读取文件: {file_path}")
            return self.process_text(text, use_deepseek, extraction_type)

        except Exception as e:
            print(f"文件读取失败: {e}")
            return {'error': str(e)}

    def _save_results(self, result: Dict[str, Any]) -> None:
        """
        保存分析结果

        Args:
            result: 分析结果
        """
        try:
            # 保存JSON结果
            json_filename = f"analysis_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            json_filepath = os.path.join(self.output_dir, json_filename)

            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"分析结果已保存到: {json_filepath}")

        except Exception as e:
            print(f"保存结果失败: {e}")

    def print_summary(self, result: Dict[str, Any]) -> None:
        """
        打印分析摘要

        Args:
            result: 分析结果
        """
        print("\n" + "="*50)
        print("分析结果摘要")
        print("="*50)

        if 'local_analysis' in result:
            local = result['local_analysis']
            basic_stats = local.get('basic_stats', {})

            print(f"文本长度: {basic_stats.get('text_length', 0)} 字符")
            print(f"词数: {basic_stats.get('word_count', 0)} 个")
            print(f"句子数: {basic_stats.get('sentence_count', 0)} 个")
            print(f"唯一词数: {basic_stats.get('unique_words', 0)} 个")

            # 数据提取统计
            data_extraction = local.get('data_extraction', {})
            print(f"\n数据提取统计:")
            print(f"  数字: {data_extraction.get('numbers_found', 0)} 个")
            print(f"  百分比: {data_extraction.get('percentages_found', 0)} 个")
            print(f"  日期: {data_extraction.get('dates_found', 0)} 个")
            print(f"  金额: {data_extraction.get('money_found', 0)} 个")
            print(f"  邮箱: {data_extraction.get('emails_found', 0)} 个")
            print(f"  电话: {data_extraction.get('phones_found', 0)} 个")
            print(f"  网址: {data_extraction.get('urls_found', 0)} 个")

            # 实体统计
            entities = local.get('entities', {})
            print(f"\n实体统计:")
            for entity_type, entity_list in entities.items():
                print(f"  {entity_type}: {len(entity_list)} 个")

            # 情感分析
            sentiment = local.get('sentiment', {})
            print(f"\n情感分析:")
            print(f"  情感倾向: {sentiment.get('sentiment_label', '未知')}")
            print(f"  情感得分: {sentiment.get('sentiment_score', 0):.2f}")
            print(f"  正面词汇: {sentiment.get('positive_count', 0)} 个")
            print(f"  负面词汇: {sentiment.get('negative_count', 0)} 个")

        # 可视化文件
        if 'visualizations' in result:
            print(f"\n生成的可视化文件:")
            for viz_type, filepath in result['visualizations'].items():
                print(f"  {viz_type}: {filepath}")

        print("="*50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='信息可视化演示程序')
    parser.add_argument('--text', type=str, help='要分析的文本内容')
    parser.add_argument('--file', type=str, help='要分析的文件路径')
    parser.add_argument('--api-key', type=str, help='DeepSeek API密钥')
    parser.add_argument('--output-dir', type=str, default='output', help='输出目录')
    parser.add_argument('--no-deepseek', action='store_true', help='不使用DeepSeek API')
    parser.add_argument('--extraction-type', type=str, default='comprehensive',
                       choices=['comprehensive', 'entities', 'sentiment', 'keywords'],
                       help='数据提取类型')

    args = parser.parse_args()

    # 检查输入
    if not args.text and not args.file:
        print("错误: 请提供要分析的文本 (--text) 或文件路径 (--file)")
        return

    # 初始化程序
    try:
        app = InfoVizDemo(args.api_key, args.output_dir)
    except Exception as e:
        print(f"初始化失败: {e}")
        return

    # 处理文本
    if args.text:
        result = app.process_text(
            args.text,
            use_deepseek=not args.no_deepseek,
            extraction_type=args.extraction_type
        )
    else:
        result = app.process_file(
            args.file,
            use_deepseek=not args.no_deepseek,
            extraction_type=args.extraction_type
        )

    # 打印摘要
    app.print_summary(result)

    print(f"\n分析完成! 结果已保存到 {args.output_dir} 目录")

if __name__ == "__main__":
    main()
