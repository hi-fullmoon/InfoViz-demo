#!/usr/bin/env python3
"""
测试脚本 - 验证信息可视化应用的基本功能
"""

import json
import os
from main import analyze_text, structure_data, generate_visualization

def test_functions():
    """测试各个函数的功能"""
    print("🧪 开始测试函数功能...")

    # 测试数据
    test_text = """
    万辰集团2024年营收达到323亿元，同比增长109.33%。
    净利润4.72亿元，同比增长50358.8%。
    门店数量15365家，覆盖全国主要城市。
    """

    # 测试文本分析函数
    print("\n1️⃣ 测试文本分析函数...")
    analysis_result = analyze_text(test_text)
    print("✅ 文本分析完成")
    print(f"分析结果: {analysis_result[:200]}...")

    # 测试数据结构化函数
    print("\n2️⃣ 测试数据结构化函数...")
    structured_data = structure_data(analysis_result)
    print("✅ 数据结构化完成")
    print(f"结构化数据: {structured_data[:200]}...")

    # 测试可视化函数
    print("\n3️⃣ 测试可视化函数...")
    echarts_config = generate_visualization(structured_data)
    print("✅ 可视化配置生成完成")
    print(f"ECharts配置: {echarts_config[:200]}...")

    # 保存测试结果
    test_results = {
        "analysis_result": json.loads(analysis_result),
        "structured_data": json.loads(structured_data),
        "echarts_config": json.loads(echarts_config)
    }

    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)

    print("\n✅ 所有函数测试完成！结果已保存到 test_results.json")
    return True

def test_data_file():
    """测试数据文件是否存在"""
    print("\n📁 检查数据文件...")

    if os.path.exists('data.txt'):
        with open('data.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ data.txt 文件存在，内容长度: {len(content)} 字符")
        return True
    else:
        print("❌ data.txt 文件不存在")
        return False

def test_environment():
    """测试环境配置"""
    print("\n🔧 检查环境配置...")

    # 检查API密钥
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    if deepseek_key and deepseek_key != "your-deepseek-api-key-here":
        print("✅ DeepSeek API密钥已配置")
        return True
    else:
        print("⚠️  DeepSeek API密钥未配置或使用默认值")
        print("   请在config.env文件中设置正确的API密钥")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试信息可视化应用")
    print("=" * 50)

    # 运行各项测试
    tests = [
        ("环境配置", test_environment),
        ("数据文件", test_data_file),
        ("函数功能", test_functions)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试失败: {str(e)}")
            results.append((test_name, False))

    # 输出测试总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n🎯 测试完成: {passed}/{total} 项测试通过")

    if passed == total:
        print("🎉 所有测试通过！应用可以正常运行。")
    else:
        print("⚠️  部分测试失败，请检查配置后重试。")

if __name__ == "__main__":
    main()
