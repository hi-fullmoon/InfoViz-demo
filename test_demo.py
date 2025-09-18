"""
快速测试脚本
验证InfoViz-demo的基本功能
"""

import os
import sys

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")

    try:
        from text_processor import TextProcessor
        print("✓ TextProcessor 导入成功")
    except ImportError as e:
        print(f"✗ TextProcessor 导入失败: {e}")
        return False

    try:
        from visualizer import DataVisualizer
        print("✓ DataVisualizer 导入成功")
    except ImportError as e:
        print(f"✗ DataVisualizer 导入失败: {e}")
        return False

    try:
        from deepseek_client import DeepSeekClient
        print("✓ DeepSeekClient 导入成功")
    except ImportError as e:
        print(f"✗ DeepSeekClient 导入失败: {e}")
        return False

    try:
        from main import InfoVizDemo
        print("✓ InfoVizDemo 导入成功")
    except ImportError as e:
        print(f"✗ InfoVizDemo 导入失败: {e}")
        return False

    return True

def test_text_processing():
    """测试文本处理功能"""
    print("\n测试文本处理功能...")

    try:
        from text_processor import TextProcessor

        processor = TextProcessor()
        sample_text = "这是一个测试文本。包含一些数字：123，百分比：50%，以及一些关键词。"

        result = processor.create_data_summary(sample_text)

        print(f"✓ 文本处理成功")
        print(f"  - 文本长度: {result['basic_stats']['text_length']}")
        print(f"  - 词数: {result['basic_stats']['word_count']}")
        print(f"  - 数字数量: {result['data_extraction']['numbers_found']}")
        print(f"  - 百分比数量: {result['data_extraction']['percentages_found']}")

        return True
    except Exception as e:
        print(f"✗ 文本处理失败: {e}")
        return False

def test_visualization():
    """测试可视化功能"""
    print("\n测试可视化功能...")

    try:
        from visualizer import DataVisualizer
        from text_processor import TextProcessor

        # 创建测试数据
        processor = TextProcessor()
        sample_text = "人工智能技术正在快速发展。机器学习、深度学习、自然语言处理等技术不断突破。"
        data_summary = processor.create_data_summary(sample_text)

        # 创建可视化器
        visualizer = DataVisualizer(output_dir="test_output")

        # 测试词云生成
        wordcloud_path = visualizer.create_word_cloud(sample_text, "测试词云")
        print(f"✓ 词云生成成功: {wordcloud_path}")

        # 测试关键词频率图
        if data_summary['top_keywords']:
            keyword_path = visualizer.create_keyword_frequency_chart(data_summary['top_keywords'])
            print(f"✓ 关键词频率图生成成功: {keyword_path}")

        return True
    except Exception as e:
        print(f"✗ 可视化测试失败: {e}")
        return False

def test_main_app():
    """测试主程序功能"""
    print("\n测试主程序功能...")

    try:
        from main import InfoVizDemo

        # 创建测试输出目录
        test_output_dir = "test_output"
        if not os.path.exists(test_output_dir):
            os.makedirs(test_output_dir)

        # 初始化应用
        app = InfoVizDemo(output_dir=test_output_dir)

        # 测试文本
        sample_text = """
        2023年，中国人工智能行业快速发展。根据统计数据显示，
        全国AI企业数量达到5000多家，同比增长25%。
        北京、上海、深圳等一线城市的AI企业数量占全国总数的60%以上。
        """

        # 处理文本（不使用DeepSeek API）
        result = app.process_text(sample_text, use_deepseek=False)

        print("✓ 主程序运行成功")
        print(f"  - 生成了 {len(result.get('visualizations', {}))} 个可视化文件")

        return True
    except Exception as e:
        print(f"✗ 主程序测试失败: {e}")
        return False

def cleanup_test_files():
    """清理测试文件"""
    print("\n清理测试文件...")

    import shutil

    test_dirs = ["test_output", "example_output"]
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            try:
                shutil.rmtree(test_dir)
                print(f"✓ 清理目录: {test_dir}")
            except Exception as e:
                print(f"✗ 清理目录失败 {test_dir}: {e}")

def main():
    """主测试函数"""
    print("InfoViz-demo 功能测试")
    print("=" * 40)

    tests = [
        test_imports,
        test_text_processing,
        test_visualization,
        test_main_app
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 40)
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！程序可以正常使用。")
    else:
        print("⚠️  部分测试失败，请检查依赖包安装。")

    # 询问是否清理测试文件
    try:
        response = input("\n是否清理测试文件？(y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            cleanup_test_files()
    except KeyboardInterrupt:
        print("\n测试完成。")

if __name__ == "__main__":
    main()
