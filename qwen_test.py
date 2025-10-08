from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# 测试不同的模型名称
models_to_try = [
    "dashscope/qwen-max",
    "dashscope/qwen-plus",
    "dashscope/qwen-turbo",
]

for model in models_to_try:
    print(f"\n🔄 测试模型: {model}")
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": "你是谁？"}]
        )
        print("✅ 成功调用：", response.choices[0].message.content)
        break
    except Exception as e:
        print(f"❌ 调用失败：{e}")
        continue
