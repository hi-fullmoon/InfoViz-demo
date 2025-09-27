/**
 * DeepSeek API客户端模块
 * 用于调用DeepSeek模型进行文本分析和数据提取
 */

import axios, { AxiosResponse } from 'axios';
import * as dotenv from 'dotenv';
import { DeepSeekResponse, ExtractedData, VisualizationSuggestion, DeepSeekClientConfig } from './types';

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
  async extractDataFromText(text: string): Promise<ExtractedData> {
    const prompt = `
分析以下文本，提取其中的数据和重要信息

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

文本内容：
${text}`;

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
  generateVisualizationSuggestions(): VisualizationSuggestion[] {
    // TODO: 实现可视化建议生成逻辑
    return [];
  }

  /**
   * 向DeepSeek API发送请求
   * @param prompt 提示词
   * @returns API响应
   */
  private async makeRequest(prompt: string): Promise<DeepSeekResponse> {
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
  private parseResponse(response: DeepSeekResponse): ExtractedData {
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
  private extractJsonFromMarkdown(content: string): string | null {
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
