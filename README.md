# 基于 CrewAI 的信息可视化应用

这是一个使用 CrewAI 框架和 DeepSeek 模型构建的智能信息可视化应用，能够自动分析文本内容并生成可视化图表。

## 功能特点

### 🔍 三阶段处理流程

1. **内容提炼阶段** - 研究员 Agent
   - 通读文章，识别核心论点
   - 提取关键数据和重要实体
   - 使用文本分析工具进行智能提取

2. **信息分析与结构化阶段** - 分析师 Agent
   - 对提炼信息进行归纳分类
   - 转换为结构化的JSON数据
   - 为可视化准备标准化数据格式

3. **可视化决策与执行阶段** - 可视化工程师 Agent
   - 根据数据特点选择合适图表类型
   - 生成ECharts配置
   - 输出可直接使用的前端可视化代码

## 安装和使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 DeepSeek API 密钥

创建 `.env` 文件并添加您的 DeepSeek API 密钥：

```bash
# 创建 .env 文件
echo "DEEPSEEK_API_KEY=your-deepseek-api-key-here" > .env
```

或者设置环境变量：

```bash
export DEEPSEEK_API_KEY=your-deepseek-api-key-here
```

**获取 DeepSeek API 密钥：**
1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 在控制台中创建 API 密钥
4. 将密钥复制到 `.env` 文件中

**重要提示：**
- 模型配置已修复为 `deepseek/deepseek-chat`
- 确保 API 密钥有效且有足够的额度
- 程序会自动检查环境变量配置

### 3. 准备数据

将您要分析的文本内容放入 `data.txt` 文件中。

### 4. 运行应用

**运行主程序:**
```bash
python main.py
# 或者
./run.sh
```
