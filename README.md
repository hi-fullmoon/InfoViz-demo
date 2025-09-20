# InfoViz-demo

一个基于 Python 的智能文本分析和可视化系统，集成了 DeepSeek AI 模型，能够从文本中提取重要信息并生成多种类型的可视化图表。

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

```bash
sh ./run.sh data.txt
```
