"""
字体修复脚本
检测和修复中文字体显示问题
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def list_available_fonts():
    """列出系统中所有可用的字体"""
    print("系统中可用的字体:")
    print("-" * 50)

    fonts = []
    for font in fm.fontManager.ttflist:
        fonts.append(font.name)

    # 去重并排序
    unique_fonts = sorted(set(fonts))

    for i, font in enumerate(unique_fonts, 1):
        print(f"{i:3d}. {font}")

    return unique_fonts

def find_chinese_fonts():
    """查找中文字体"""
    print("\n中文字体:")
    print("-" * 50)

    chinese_fonts = []
    keywords = ['chinese', 'cjk', 'han', 'ping', 'hei', 'song', 'kai', 'ming', 'noto', 'source']

    for font in fm.fontManager.ttflist:
        font_name = font.name
        if any(keyword in font_name.lower() for keyword in keywords):
            chinese_fonts.append(font_name)
            print(f"✓ {font_name}")

    # 检查常见的中文字体
    common_fonts = [
        'PingFang SC',
        'Hiragino Sans GB',
        'STHeiti',
        'SimHei',
        'Microsoft YaHei',
        'Arial Unicode MS',
        'Noto Sans CJK SC',
        'Source Han Sans SC'
    ]

    print("\n常见中文字体检查:")
    print("-" * 50)
    for font in common_fonts:
        if font in [f.name for f in fm.fontManager.ttflist]:
            print(f"✓ {font} - 可用")
        else:
            print(f"✗ {font} - 不可用")

    return chinese_fonts

def test_font_rendering():
    """测试字体渲染"""
    print("\n字体渲染测试:")
    print("-" * 50)

    # 测试文本
    test_text = "中文测试：人工智能、机器学习、深度学习"

    # 获取当前字体设置
    current_font = plt.rcParams['font.sans-serif'][0]
    print(f"当前字体: {current_font}")

    # 创建测试图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.5, test_text, fontsize=16, ha='center', va='center')
    ax.set_title(f"字体测试 - {current_font}", fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 保存测试图
    test_file = "font_test.png"
    plt.savefig(test_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"测试图片已保存为: {test_file}")
    return test_file

def fix_font_config():
    """修复字体配置"""
    print("\n修复字体配置:")
    print("-" * 50)

    # 查找最佳中文字体
    best_font = None
    common_fonts = ['PingFang SC', 'Hiragino Sans GB', 'STHeiti', 'SimHei', 'Microsoft YaHei']

    for font in common_fonts:
        if font in [f.name for f in fm.fontManager.ttflist]:
            best_font = font
            break

    if best_font:
        print(f"选择字体: {best_font}")

        # 更新matplotlib配置
        plt.rcParams['font.sans-serif'] = [best_font, 'DejaVu Sans', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False

        # 清除字体缓存
        try:
            fm._rebuild()
        except AttributeError:
            # 新版本的matplotlib可能没有_rebuild方法
            pass

        print("字体配置已更新")
        return best_font
    else:
        print("未找到合适的中文字体")
        return None

def main():
    """主函数"""
    print("字体检测和修复工具")
    print("=" * 60)

    # 列出所有字体
    all_fonts = list_available_fonts()
    print(f"\n总共找到 {len(all_fonts)} 个字体")

    # 查找中文字体
    chinese_fonts = find_chinese_fonts()
    print(f"\n找到 {len(chinese_fonts)} 个中文字体")

    # 修复字体配置
    best_font = fix_font_config()

    # 测试字体渲染
    if best_font:
        test_file = test_font_rendering()
        print(f"\n请查看 {test_file} 文件来确认字体显示效果")

    print("\n修复完成！")
    print("如果字体显示仍有问题，请尝试:")
    print("1. 安装中文字体包")
    print("2. 重启Python环境")
    print("3. 清除matplotlib字体缓存: rm -rf ~/.matplotlib")

if __name__ == "__main__":
    main()
