"""
使用示例
演示如何使用InfoViz-demo进行文本分析和可视化
"""

from main import InfoVizDemo
import os

def example_1_basic_usage():
    """示例1: 基本使用"""
    print("示例1: 基本使用")
    print("-" * 30)

    # 示例文本
    sample_text = """
    2023年，中国人工智能行业继续保持快速发展态势。根据最新统计数据显示，
    全国AI企业数量达到5000多家，同比增长25%。其中，北京、上海、深圳等一线城市
    的AI企业数量占全国总数的60%以上。

    在技术发展方面，深度学习、自然语言处理、计算机视觉等核心技术不断突破。
    百度、阿里巴巴、腾讯等科技巨头在AI领域投入超过1000亿元，推动行业快速发展。

    市场前景方面，预计到2025年，中国AI市场规模将达到2000亿元，年复合增长率
    超过30%。政府政策支持、资本投入增加、技术人才储备丰富等因素为行业发展
    提供了有力支撑。
    """

    # 初始化程序（不使用DeepSeek API）
    app = InfoVizDemo(output_dir="example_output")

    # 处理文本
    result = app.process_text(sample_text, use_deepseek=False)

    # 打印摘要
    app.print_summary(result)

    print("示例1完成！\n")

def example_2_with_deepseek():
    """示例2: 使用DeepSeek API"""
    print("示例2: 使用DeepSeek API")
    print("-" * 30)

    # 检查API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("未设置DEEPSEEK_API_KEY环境变量，跳过此示例")
        return

    # 示例文本
    sample_text = """
    苹果公司2023年第四季度财报显示，公司营收达到1196亿美元，同比增长8%。
    iPhone销量为7830万部，Mac销量为690万台，iPad销量为1410万台。

    在服务业务方面，App Store、iCloud、Apple Music等服务收入达到231亿美元，
    同比增长16%。Apple Pay交易量增长显著，月活跃用户超过5亿。

    公司CEO蒂姆·库克表示，尽管面临宏观经济挑战，但苹果在创新和用户体验方面
    的持续投入为公司带来了强劲的业绩表现。未来将继续投资于AR/VR、人工智能
    和芯片技术等领域。
    """

    # 初始化程序
    app = InfoVizDemo(api_key=api_key, output_dir="example_output")

    # 处理文本
    result = app.process_text(sample_text, use_deepseek=True, extraction_type="comprehensive")

    # 打印摘要
    app.print_summary(result)

    print("示例2完成！\n")

def example_3_file_processing():
    """示例3: 文件处理"""
    print("示例3: 文件处理")
    print("-" * 30)

    # 创建示例文件
    sample_file_content = """
    新能源汽车市场分析报告

    2023年，全球新能源汽车销量达到1400万辆，同比增长35%。中国作为全球最大的
    新能源汽车市场，销量达到950万辆，占全球总销量的68%。

    主要品牌表现：
    - 比亚迪：销量302万辆，同比增长62%
    - 特斯拉：销量180万辆，同比增长38%
    - 蔚来：销量16万辆，同比增长81%
    - 理想：销量37万辆，同比增长182%

    技术发展趋势：
    1. 电池技术：磷酸铁锂电池占比提升至65%
    2. 充电技术：800V高压快充技术逐步普及
    3. 智能化：L2级自动驾驶渗透率达到45%

    市场预测：预计2024年全球新能源汽车销量将达到1800万辆，同比增长29%。
    """

    # 创建示例文件
    sample_file_path = "sample_report.txt"
    with open(sample_file_path, 'w', encoding='utf-8') as f:
        f.write(sample_file_content)

    try:
        # 初始化程序
        app = InfoVizDemo(output_dir="example_output")

        # 处理文件
        result = app.process_file(sample_file_path, use_deepseek=False)

        # 打印摘要
        app.print_summary(result)

    finally:
        # 清理示例文件
        if os.path.exists(sample_file_path):
            os.remove(sample_file_path)

    print("示例3完成！\n")

def example_4_different_extraction_types():
    """示例4: 不同的提取类型"""
    print("示例4: 不同的提取类型")
    print("-" * 30)

    sample_text = """
    人工智能技术正在改变我们的生活方式。从智能手机的语音助手到自动驾驶汽车，
    从医疗诊断到金融风控，AI技术的应用越来越广泛。

    然而，AI技术的发展也带来了一些挑战。数据隐私保护、算法偏见、就业影响
    等问题需要认真对待。我们需要在推动技术发展的同时，确保AI技术的安全、
    可靠和公平。

    未来，AI技术将继续快速发展。量子计算、脑机接口、通用人工智能等前沿
    技术有望取得重大突破，为人类社会发展带来新的机遇。
    """

    extraction_types = ['comprehensive', 'entities', 'sentiment', 'keywords']

    for extraction_type in extraction_types:
        print(f"提取类型: {extraction_type}")

        app = InfoVizDemo(output_dir=f"example_output_{extraction_type}")
        result = app.process_text(sample_text, use_deepseek=False, extraction_type=extraction_type)

        # 只打印关键信息
        if 'local_analysis' in result:
            local = result['local_analysis']
            print(f"  文本长度: {local.get('basic_stats', {}).get('text_length', 0)} 字符")
            print(f"  情感倾向: {local.get('sentiment', {}).get('sentiment_label', '未知')}")
            print(f"  关键词数量: {len(local.get('top_keywords', []))}")

        print()

def main():
    """运行所有示例"""
    print("InfoViz-demo 使用示例")
    print("=" * 50)

    # 运行示例
    example_1_basic_usage()
    example_2_with_deepseek()
    example_3_file_processing()
    example_4_different_extraction_types()

    print("所有示例运行完成！")
    print("请查看 example_output 目录中的生成文件")

if __name__ == "__main__":
    main()
