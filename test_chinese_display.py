#!/usr/bin/env python3
"""
测试中文字体显示效果
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

def test_chinese_fonts():
    """测试中文字体显示"""
    print("测试中文字体显示效果...")

    # 查找中文字体
    chinese_fonts = []
    for font in fm.fontManager.ttflist:
        font_name = font.name
        if any(keyword in font_name.lower() for keyword in ['chinese', 'cjk', 'han', 'ping', 'hei', 'song', 'kai', 'ming', 'hiragino', 'stheit']):
            chinese_fonts.append(font_name)

    print(f"找到 {len(chinese_fonts)} 个中文字体:")
    for font in chinese_fonts[:10]:  # 显示前10个
        print(f"  - {font}")

    # 设置字体
    common_fonts = ['Hiragino Sans GB', 'Hiragino Sans', 'STHeiti', 'PingFang SC', 'Arial Unicode MS']
    selected_font = 'DejaVu Sans'

    for font in common_fonts:
        if font in [f.name for f in fm.fontManager.ttflist]:
            selected_font = font
            break

    plt.rcParams['font.sans-serif'] = [selected_font, 'Hiragino Sans GB', 'STHeiti', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    print(f"使用字体: {selected_font}")

    # 创建测试图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 测试数据
    categories = ['人工智能', '机器学习', '深度学习', '自然语言处理', '计算机视觉']
    values = [85, 78, 92, 88, 76]

    # 柱状图
    bars = ax1.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax1.set_title('中文显示测试 - 技术领域热度', fontsize=16, fontweight='bold')
    ax1.set_xlabel('技术领域', fontsize=12)
    ax1.set_ylabel('热度指数', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)

    # 添加数值标签
    for bar, value in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(value), ha='center', va='bottom', fontsize=10)

    # 饼图
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    wedges, texts, autotexts = ax2.pie(values, labels=categories, autopct='%1.1f%%',
                                       colors=colors, startangle=90)
    ax2.set_title('技术领域分布', fontsize=16, fontweight='bold')

    # 调整布局
    plt.tight_layout()

    # 保存图片
    output_file = "chinese_display_test.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"测试图片已保存为: {output_file}")
    return output_file

if __name__ == "__main__":
    test_chinese_fonts()
    print("中文字体测试完成！")
