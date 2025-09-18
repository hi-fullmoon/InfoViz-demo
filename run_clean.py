"""
清洁版运行脚本
抑制字体警告，提供更好的用户体验
"""

import warnings
import os
import sys

# 抑制matplotlib字体警告
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*missing from font.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, message='.*invalid value encountered.*')

# 设置matplotlib后端
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

def main():
    """主函数"""
    print("InfoViz Demo - Clean Version")
    print("=" * 40)

    # 检查参数
    if len(sys.argv) < 2:
        print("Usage: python run_clean.py <file_path> [--no-deepseek]")
        print("Example: python run_clean.py test.txt --no-deepseek")
        return

    file_path = sys.argv[1]
    use_deepseek = "--no-deepseek" not in sys.argv

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return

    try:
        # 导入并运行英文版程序
        from main_en import InfoVizDemoEN

        print(f"Processing file: {file_path}")
        print(f"Using DeepSeek API: {use_deepseek}")
        print("-" * 40)

        # 初始化程序
        app = InfoVizDemoEN(output_dir="output")

        # 处理文件
        result = app.process_file(file_path, use_deepseek=use_deepseek)

        # 打印摘要
        app.print_summary(result)

        print("\n✅ Analysis completed successfully!")
        print("📊 Check the 'output' directory for generated visualizations")

    except Exception as e:
        print(f"❌ Error: {e}")
        return

if __name__ == "__main__":
    main()
