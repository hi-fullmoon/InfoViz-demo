# 信息可视化演示程序 - TypeScript 版本

## 安装和运行

### 1. 安装依赖

```bash
pnpm install
```

### 2. 配置环境变量

复制 `env.example` 文件为 `.env` 并设置你的 DeepSeek API 密钥：

```bash
cp env.example .env
# 编辑 .env 文件，设置 DEEPSEEK_API_KEY
```

### 3. 运行

```bash
# 运行程序
pnpm start --text "你的文本内容"
# 或者
pnpm start --file data.txt
```
