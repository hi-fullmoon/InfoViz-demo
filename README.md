# InfoViz-demo

一个基于 Python 的智能文本分析和可视化系统，集成了 DeepSeek AI 模型，能够从文本中提取重要信息并生成多种类型的可视化图表。

## 功能特性

- 🤖 **DeepSeek AI 集成**: 使用 DeepSeek 模型进行智能文本分析
- 📊 **多种可视化**: 支持词云、柱状图、饼图、交互式仪表板等
- 🔍 **智能数据提取**: 自动识别数字、日期、实体、情感等信息
- 📈 **实时分析**: 快速处理文本并生成可视化结果
- 🎨 **美观界面**: 现代化的图表设计和配色方案

## 安装说明

1. 克隆项目到本地：

```bash
git clone <repository-url>
cd InfoViz-demo
```

2. 安装依赖包：

```bash
pip install -r requirements.txt
```

3. 配置 API 密钥：

```bash
# 复制配置文件
cp config_example.env .env

# 编辑.env文件，填入您的DeepSeek API密钥
DEEPSEEK_API_KEY=your_api_key_here
```

## 使用方法

### 推荐使用方式（清洁版）

1. **分析文件**（推荐）：

```bash
python run_clean.py test.txt --no-deepseek
```

2. **使用启动脚本**：

```bash
./run.sh --file "test.txt" --no-deepseek
```

### 其他使用方式

1. **分析文本内容**：

```bash
python main.py --text "您的文本内容"
```

2. **分析文件**：

```bash
python main.py --file "path/to/your/file.txt"
```

3. **不使用 DeepSeek API**（仅本地分析）：

```bash
python main.py --text "您的文本内容" --no-deepseek
```

4. **指定提取类型**：

```bash
python main.py --text "您的文本内容" --extraction-type entities
```

5. **英文版程序**（避免中文字体问题）：

```bash
python main_en.py --file "test.txt" --no-deepseek
```

### 编程使用

```python
from main import InfoVizDemo

# 初始化
app = InfoVizDemo(api_key="your_api_key")

# 分析文本
result = app.process_text("您的文本内容")

# 打印结果摘要
app.print_summary(result)
```

### 运行示例

```bash
python example_usage.py
```

## 支持的分析类型

- `comprehensive`: 综合分析（默认）
- `entities`: 实体提取
- `sentiment`: 情感分析
- `keywords`: 关键词提取

## 生成的可视化类型

1. **词云图**: 显示文本中的高频词汇
2. **关键词频率图**: 柱状图显示关键词出现频率
3. **实体分布图**: 饼图显示不同类型实体的分布
4. **情感分析图**: 显示文本的情感倾向
5. **数据摘要图**: 综合展示所有提取的数据
6. **交互式仪表板**: HTML 格式的交互式可视化

## 输出文件

程序会在指定的输出目录中生成以下文件：

- `analysis_result_*.json`: 完整的分析结果
- `wordcloud_*.png`: 词云图
- `keyword_frequency_*.png`: 关键词频率图
- `entity_distribution_*.png`: 实体分布图
- `sentiment_analysis_*.png`: 情感分析图
- `data_summary_*.png`: 数据摘要图
- `interactive_dashboard_*.html`: 交互式仪表板

## 项目结构

```
InfoViz-demo/
├── main.py                 # 主程序入口
├── deepseek_client.py      # DeepSeek API客户端
├── text_processor.py       # 文本处理器
├── visualizer.py          # 可视化器
├── example_usage.py       # 使用示例
├── requirements.txt       # 依赖包列表
├── config_example.env     # 配置文件示例
└── README.md             # 项目说明
```

## 依赖包

- `openai`: DeepSeek API 调用
- `matplotlib`: 基础图表绘制
- `seaborn`: 统计图表
- `plotly`: 交互式图表
- `pandas`: 数据处理
- `jieba`: 中文分词
- `wordcloud`: 词云生成
- `python-dotenv`: 环境变量管理

## 字体问题解决方案

如果遇到中文字体显示问题，可以使用以下解决方案：

1. **使用清洁版程序**（推荐）：

```bash
python run_clean.py test.txt --no-deepseek
```

2. **使用英文版程序**：

```bash
python main_en.py --file "test.txt" --no-deepseek
```

3. **手动修复字体**：

```bash
python fix_chinese_fonts.py
```

## 注意事项

1. 使用 DeepSeek API 需要有效的 API 密钥
2. 确保网络连接正常，API 调用需要访问外部服务
3. 生成的图片文件较大，建议定期清理输出目录
4. 中文文本分析效果最佳，英文文本也支持
5. 如果遇到字体显示问题，建议使用清洁版或英文版程序

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！
