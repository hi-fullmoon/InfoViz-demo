"""
英文版主程序入口
使用英文标签避免中文字体显示问题
"""

import os
import json
import argparse
from typing import Dict, Any, Optional
from datetime import datetime

from deepseek_client import DeepSeekClient
from text_processor import TextProcessor
from visualizer_en import DataVisualizerEN

class InfoVizDemoEN:
    """英文版信息可视化演示主类"""

    def __init__(self, api_key: Optional[str] = None, output_dir: str = "output"):
        """
        初始化信息可视化演示

        Args:
            api_key: DeepSeek API密钥
            output_dir: 输出目录
        """
        self.deepseek_client = DeepSeekClient(api_key)
        self.text_processor = TextProcessor()
        self.visualizer = DataVisualizerEN(output_dir)
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
        print("Starting text processing...")

        # 本地文本处理
        print("1. Performing local text analysis...")
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
                print("2. Calling DeepSeek API for deep analysis...")
                deepseek_data = self.deepseek_client.extract_data_from_text(text, extraction_type)
                result['deepseek_analysis'] = deepseek_data

                # 生成可视化建议
                print("3. Generating visualization suggestions...")
                viz_suggestions = self.deepseek_client.generate_visualization_suggestions(deepseek_data)
                result['visualization_suggestions'] = viz_suggestions

            except Exception as e:
                print(f"DeepSeek API call failed: {e}")
                result['deepseek_error'] = str(e)

        # 生成可视化图表
        print("4. Generating visualization charts...")
        try:
            visualizations = self.visualizer.generate_all_visualizations(
                local_summary, text
            )
            result['visualizations'] = visualizations
            print(f"Generated {len(visualizations)} visualization charts")
        except Exception as e:
            print(f"Visualization generation failed: {e}")
            result['visualization_error'] = str(e)

        # 保存结果
        print("5. Saving analysis results...")
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

            print(f"Successfully read file: {file_path}")
            return self.process_text(text, use_deepseek, extraction_type)

        except Exception as e:
            print(f"File reading failed: {e}")
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

            print(f"Analysis results saved to: {json_filepath}")

        except Exception as e:
            print(f"Failed to save results: {e}")

    def print_summary(self, result: Dict[str, Any]) -> None:
        """
        打印分析摘要

        Args:
            result: 分析结果
        """
        print("\n" + "="*50)
        print("Analysis Results Summary")
        print("="*50)

        if 'local_analysis' in result:
            local = result['local_analysis']
            basic_stats = local.get('basic_stats', {})

            print(f"Text Length: {basic_stats.get('text_length', 0)} characters")
            print(f"Word Count: {basic_stats.get('word_count', 0)} words")
            print(f"Sentence Count: {basic_stats.get('sentence_count', 0)} sentences")
            print(f"Unique Words: {basic_stats.get('unique_words', 0)} unique words")

            # 数据提取统计
            data_extraction = local.get('data_extraction', {})
            print(f"\nData Extraction Statistics:")
            print(f"  Numbers: {data_extraction.get('numbers_found', 0)} found")
            print(f"  Percentages: {data_extraction.get('percentages_found', 0)} found")
            print(f"  Dates: {data_extraction.get('dates_found', 0)} found")
            print(f"  Money: {data_extraction.get('money_found', 0)} found")
            print(f"  Emails: {data_extraction.get('emails_found', 0)} found")
            print(f"  Phones: {data_extraction.get('phones_found', 0)} found")
            print(f"  URLs: {data_extraction.get('urls_found', 0)} found")

            # 实体统计
            entities = local.get('entities', {})
            print(f"\nEntity Statistics:")
            for entity_type, entity_list in entities.items():
                print(f"  {entity_type}: {len(entity_list)} found")

            # 情感分析
            sentiment = local.get('sentiment', {})
            print(f"\nSentiment Analysis:")
            print(f"  Sentiment: {sentiment.get('sentiment_label', 'Unknown')}")
            print(f"  Sentiment Score: {sentiment.get('sentiment_score', 0):.2f}")
            print(f"  Positive Words: {sentiment.get('positive_count', 0)} words")
            print(f"  Negative Words: {sentiment.get('negative_count', 0)} words")

        # 可视化文件
        if 'visualizations' in result:
            print(f"\nGenerated Visualization Files:")
            for viz_type, filepath in result['visualizations'].items():
                print(f"  {viz_type}: {filepath}")

        print("="*50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='English Version InfoViz Demo Program')
    parser.add_argument('--text', type=str, help='Text content to analyze')
    parser.add_argument('--file', type=str, help='File path to analyze')
    parser.add_argument('--api-key', type=str, help='DeepSeek API key')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory')
    parser.add_argument('--no-deepseek', action='store_true', help='Do not use DeepSeek API')
    parser.add_argument('--extraction-type', type=str, default='comprehensive',
                       choices=['comprehensive', 'entities', 'sentiment', 'keywords'],
                       help='Data extraction type')

    args = parser.parse_args()

    # 检查输入
    if not args.text and not args.file:
        print("Error: Please provide text to analyze (--text) or file path (--file)")
        return

    # 初始化程序
    try:
        app = InfoVizDemoEN(args.api_key, args.output_dir)
    except Exception as e:
        print(f"Initialization failed: {e}")
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

    print(f"\nAnalysis completed! Results saved to {args.output_dir} directory")

if __name__ == "__main__":
    main()
