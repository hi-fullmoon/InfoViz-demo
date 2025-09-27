/**
 * DeepSeek API客户端模块
 * 用于调用DeepSeek模型进行文本分析和数据提取
 */

import axios, { AxiosResponse } from 'axios';
import * as dotenv from 'dotenv';
import { DeepSeekResponse, DeepSeekClientConfig } from './types';

// 加载环境变量
dotenv.config();

export class DeepSeekClient {
  private apiKey: string;
  private baseUrl: string;
  private timeout: number;

  constructor(config?: DeepSeekClientConfig) {
    this.apiKey = config?.apiKey || process.env.DEEPSEEK_API_KEY || '';
    if (!this.apiKey) {
      throw new Error('请设置DEEPSEEK_API_KEY环境变量或直接传入apiKey参数');
    }

    this.baseUrl = config?.baseUrl || 'https://api.deepseek.com/chat/completions';
    this.timeout = config?.timeout || 120000;
  }

  /**
   * 从文本中提取数据和重要信息
   * @param text 要分析的文本
   * @returns 提取的数据字典
   */
  async extractDataFromText(text: string) {
    const prompt = `
分析以下文本，提取其中的数据和重要信息：
${text}

提取要求：
1. 数据焦点：重点提取可以量化或对比的数据点。
2. 关系明确：清晰标注数据点之间的关系（例如：分类、时间序列、占比等）。
3. 信息来源：对于每个数据点，简要说明它在文本中代表的意义。

请直接以结构化的JSON格式返回，确保信息足够清晰且便于后续处理。

示例如下：
1. 如果段落中有指标数值相关，如下：
国家外汇管理局9月7日公布的数据显示，截至2025年8月末，我国外汇储备规模为33221.54亿美元，较7月末增加299.19亿美元，升幅为0.91%。
则返回：
\`\`\`json
{
  "event_summary": "中国外汇储备规模在2025年8月末的变化。",
  "source": "国家外汇管理局",
  "data_as_of": "09-07",
  "visualization_type": "chart",
  "data_points": [
    {
      "period_end": "2025年8月末",
      "value_usd_billion": 33221.54,
      "description": "期末外汇储备总规模"
    },
    {
      "period_end": "2025年7月末",
      "value_usd_billion": 32922.35,
      "description": "上期外汇储备总规模（33221.54 - 299.19）"
    }
  ]
}
\`\`\`

2. 如果段落中没有指标数值相关，如下：
国家外汇局表示，2025年8月，受主要经济体货币政策预期、宏观经济数据等因素影响，美元指数下跌，全球金融资产价格总体上涨。汇率折算和资产价格变化等因素综合作用，当月外汇储备规模上升。
则返回：
\`\`\`json
{
  "event_summary": "国家外汇储备规模上升",
  "source": "国家外汇局",
  "data_as_of": "09-07",
  "visualization_type": "card",
  "event_list": [
    {
      "event_time": "2025年8月",
      "metric_name": "美元指数",
      "action": "下跌",
      "category": "市场表现",
    },
    {
      "event_time": "2025年8月",
      "metric_name": "全球金融资产价格",
      "action": "总体上涨",
      "category": "市场表现",
    },
    {
      "event_time": "2025年8月",
      "metric_name": "外汇储备规模",
      "action": "上升",

    }
  ]
}
\`\`\`

其中 event_summary（事件摘要），source（数据来源），data_as_of（数据日期），ui（可视化类型，card 或 chart）是必填项，其他项根据实际情况选择。
`;

    try {
      const response = await this.makeRequest(prompt);
      return this.parseResponse(response);
    } catch (error) {
      console.error('数据提取失败:', error);
      throw error;
    }
  }

  /**
   * 基于提取的数据生成可视化建议
   * @param extractedData 提取的数据
   * @returns 可视化建议列表
   */
  async generateVisualizationSuggestions(extractedData: any) {
    const prompt = `
**【角色与任务目标】**
你是一个专业的数据分析师和可视化专家。请仔细分析我提供的文本内容，并完成以下任务：

1.  **提取关键数据和结论。**
2.  **判断最佳展示类型：** 判断提取的信息更适合以**ECharts 图表**展示 (类型: \`chart\`)，还是以**卡片摘要**展示 (类型: \`ui\`)。
3.  **生成格式化 JSON 输出：** 严格根据你判断的类型，生成对应的 JSON 结构。

---

### **步骤一：分析提取的数据，是一个 json 格式**

${JSON.stringify(extractedData)}

---

### **步骤二：生成可视化配置 (JSON 格式)**

请仅输出一个完整的 JSON 对象，该对象必须包含 \`visualization_type\` 字段，并根据其值决定后续的字段结构。

**结构要求：**

#### **场景 1: 如果判断类型为图表 (Chart)**
* **\`visualization_type\`** 必须为 \`"chart"\`。
* 必须包含一个 **\`echarts_options\`** 字段，其值为一个完整的 ECharts Options **JavaScript 对象结构** (JSON)。
* \`echarts_options\` 中**不**得包含任何 \`theme\`、\`color\` 属性或任何与主题相关的配置。

#### **场景 2: 如果判断类型为摘要 (UI)**
* **\`visualization_type\`** 必须为 \`"ui"\`。
* 必须包含 **\`ui_data\`** 字段，其值是一个对象，至少包含 \`title\` 和 \`summary\` 字段。

**最终 JSON 输出：**

输出示例：
\`\`\`json
{
  "visualization_type": "chart",
  "chart_suggestion": "柱状图 (Bar Chart)",
  "echarts_options": {
    "title": {"text": "年度销售额对比"},
    "tooltip": {},
    "legend": {"data": ["销售额"]},
    "xAxis": {"data": ["2023", "2024"]},
    "yAxis": {},
    "series": [{"name": "销售额", "type": "bar", "data": [120, 200]}]
  }
}

{
  "visualization_type": "ui",
  "ui_data": {
    "title": "重要政策宣布",
    "summary": "管理层宣布了一项重大的人事变动，任命了新的首席技术官，以推动未来的数字化转型战略。",
    "key_takeaways": ["人事变动", "数字化转型战略"]
  }
}
\`\`\`
    `;
    const response = await this.makeRequest(prompt);
    return this.parseResponse(response);
  }

  /**
   * 向DeepSeek API发送请求
   * @param prompt 提示词
   * @returns API响应
   */
  private async makeRequest(prompt: string) {
    const payload = {
      model: 'deepseek-chat',
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 4000,
    };

    try {
      const response: AxiosResponse<DeepSeekResponse> = await axios.post(this.baseUrl, payload, {
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        timeout: this.timeout,
      });

      if (response.status !== 200) {
        throw new Error(`API请求失败: ${response.status} - ${JSON.stringify(response.data)}`);
      }

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API请求失败: ${error.response?.status} - ${JSON.stringify(error.response?.data)}`);
      }
      throw error;
    }
  }

  /**
   * 解析API响应
   * @param response API响应
   * @returns 解析后的数据
   */
  private parseResponse(response: DeepSeekResponse) {
    try {
      // 提取AI生成的内容
      const content = response.choices[0].message.content;

      // 尝试解析JSON格式的内容
      try {
        return JSON.parse(content);
      } catch (jsonError) {
        // 如果直接解析失败，尝试提取markdown代码块中的JSON
        const jsonContent = this.extractJsonFromMarkdown(content);
        if (jsonContent) {
          try {
            return JSON.parse(jsonContent);
          } catch (jsonParseError) {
            // 如果仍然解析失败，返回原始内容
            return { content, format: 'text' } as any;
          }
        }

        // 如果都不是有效的JSON，返回原始内容
        return { content, format: 'text' } as any;
      }
    } catch (error) {
      throw new Error(`响应解析失败: ${error}`);
    }
  }

  /**
   * 从markdown代码块中提取JSON内容
   * @param content 包含markdown代码块的字符串
   * @returns 提取的JSON字符串，如果没有找到则返回null
   */
  private extractJsonFromMarkdown(content: string) {
    // 匹配 ```json ... ``` 格式的代码块
    const jsonPattern = /```json\s*\n(.*?)\n```/s;
    const jsonMatch = content.match(jsonPattern);

    if (jsonMatch) {
      return jsonMatch[1].trim();
    }

    // 如果没有找到json标记的代码块，尝试匹配任何代码块
    const codePattern = /```\s*\n(.*?)\n```/s;
    const codeMatch = content.match(codePattern);

    if (codeMatch) {
      return codeMatch[1].trim();
    }

    return null;
  }
}
