"""
强制修复中文字体显示问题
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def force_set_chinese_font():
    """强制设置中文字体"""
    # 清除matplotlib字体缓存
    cache_dir = os.path.expanduser('~/.matplotlib')
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
        print("已清除matplotlib字体缓存")

    # 强制设置字体
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'STHeiti', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 重新构建字体缓存
    fm._load_fontmanager(try_read_cache=False)

    print("字体设置已更新")
    print(f"当前字体设置: {plt.rcParams['font.sans-serif']}")

def test_chinese_display():
    """测试中文显示"""
    import numpy as np

    # 创建测试图
    fig, ax = plt.subplots(figsize=(10, 6))

    # 测试数据
    categories = ['人工智能', '机器学习', '深度学习', '自然语言处理', '计算机视觉']
    values = [85, 78, 92, 88, 76]

    # 创建柱状图
    bars = ax.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])

    # 设置标题和标签
    ax.set_title('中文显示测试 - 技术领域热度', fontsize=16, fontweight='bold')
    ax.set_xlabel('技术领域', fontsize=12)
    ax.set_ylabel('热度指数', fontsize=12)

    # 添加数值标签
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(value), ha='center', va='bottom', fontsize=10)

    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')

    # 调整布局
    plt.tight_layout()

    # 保存图片
    test_file = "chinese_font_test.png"
    plt.savefig(test_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"测试图片已保存为: {test_file}")
    return test_file

if __name__ == "__main__":
    print("强制修复中文字体显示问题")
    print("=" * 40)

    force_set_chinese_font()
    test_file = test_chinese_display()

    print("\n修复完成！")
    print(f"请查看 {test_file} 文件确认中文显示效果")
