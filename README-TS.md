# 信息可视化演示程序 - TypeScript 版本

这是原 Python 项目的 TypeScript 重写版本，提供相同的功能但使用 TypeScript 实现。

## 功能特性

- 使用 DeepSeek API 进行文本分析
- 从文本中提取结构化数据
- 生成可视化建议
- 保存分析结果到 JSON 文件
- 命令行接口支持

## 项目结构

```
src/
├── types.ts              # TypeScript 类型定义
├── deepseek-client.ts    # DeepSeek API 客户端
├── infoviz-demo.ts       # 主业务逻辑类
└── main.ts               # 程序入口和命令行接口
```

## 安装和运行

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

复制 `env.example` 文件为 `.env` 并设置你的 DeepSeek API 密钥：

```bash
cp env.example .env
# 编辑 .env 文件，设置 DEEPSEEK_API_KEY
```

### 3. 编译和运行

```bash
# 编译 TypeScript
npm run build

# 运行程序
npm start -- --text "你的文本内容"
# 或者
npm start -- --file data.txt
```

### 4. 开发模式

```bash
# 直接运行 TypeScript（需要 ts-node）
npm run dev -- --text "你的文本内容"
```

## 使用方法

### 命令行参数

- `--text <text>`: 要分析的文本内容
- `--file <file>`: 要分析的文件路径
- `--api-key <key>`: DeepSeek API 密钥（可选，也可通过环境变量设置）
- `--output-dir <dir>`: 输出目录（默认：output）

### 示例

```bash
# 分析文本
npm start -- --text "国家外汇管理局9月7日公布的数据显示..."

# 分析文件
npm start -- --file data.txt

# 指定输出目录
npm start -- --file data.txt --output-dir results
```

## 开发

### 代码检查

```bash
npm run lint
```

### 测试

```bash
npm test
```

### 清理

```bash
npm run clean
```

## 与 Python 版本的对比

| 特性     | Python 版本            | TypeScript 版本    |
| -------- | ---------------------- | ------------------ |
| 类型安全 | 部分（类型注解）       | 完全（编译时检查） |
| 性能     | 解释执行               | 编译后执行         |
| 依赖管理 | pip + requirements.txt | npm + package.json |
| 错误处理 | 运行时                 | 编译时 + 运行时    |
| 开发体验 | 良好                   | 优秀（IDE 支持）   |

## 注意事项

1. 确保已安装 Node.js 16+ 版本
2. 需要有效的 DeepSeek API 密钥
3. 输出目录会自动创建
4. 所有分析结果都会保存为 JSON 格式
