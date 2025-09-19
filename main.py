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
        self.output_dir = output_dir

    def process_text(self, text: str, extraction_type: str = "comprehensive") -> Dict[str, Any]:
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

        result = {
            'input_text': text,
            'deepseek_analysis': None,
            'visualization_suggestions': None
        }

        try:
            print("1. 调用DeepSeek API进行深度分析...")
            deepseek_data = self.deepseek_client.extract_data_from_text(text, extraction_type)
            result['deepseek_analysis'] = deepseek_data

            print("2. 生成可视化建议...")
            viz_suggestions = self.deepseek_client.generate_visualization_suggestions(deepseek_data)
            result['visualization_suggestions'] = viz_suggestions

        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            result['deepseek_error'] = str(e)

         # 保存结果
        print("3. 保存分析结果...")
        self.save_results(result)

        return result

    def process_file(self, file_path: str, extraction_type: str = "comprehensive") -> Dict[str, Any]:
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
            return self.process_text(text, extraction_type)

        except Exception as e:
            print(f"文件读取失败: {e}")
            return {'error': str(e)}

    def save_results(self, result: Dict[str, Any]) -> None:
        """
        保存分析结果

        Args:
            result: 分析结果
        """
        try:
            # 确保输出目录存在
            os.makedirs(self.output_dir, exist_ok=True)

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
        pass
        # TODO

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='信息可视化演示程序')
    parser.add_argument('--text', type=str, help='要分析的文本内容')
    parser.add_argument('--file', type=str, help='要分析的文件路径')
    parser.add_argument('--api-key', type=str, help='DeepSeek API密钥')
    parser.add_argument('--output-dir', type=str, default='output', help='输出目录')
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
            extraction_type=args.extraction_type
        )
    else:
        result = app.process_file(
            args.file,
            extraction_type=args.extraction_type
        )

    # 打印摘要
    app.print_summary(result)

    print(f"\n分析完成! 结果已保存到 {args.output_dir} 目录")

if __name__ == "__main__":
    main()
