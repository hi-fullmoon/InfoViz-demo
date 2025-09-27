/**
 * 信息可视化演示主类
 * 整合DeepSeek API调用、文本处理和数据可视化功能
 */

import * as fs from 'fs';
import * as path from 'path';
import { DeepSeekClient } from './deepseek-client';
import { AnalysisResult, InfoVizDemoConfig } from './types';

export class InfoVizDemo {
  private deepseekClient: DeepSeekClient;
  private outputDir: string;

  constructor(config?: InfoVizDemoConfig) {
    this.deepseekClient = new DeepSeekClient({ apiKey: config?.apiKey });
    this.outputDir = config?.outputDir || 'output';
  }

  /**
   * 处理文本并生成可视化
   * @param text 输入文本
   * @returns 处理结果
   */
  async processText(text: string): Promise<AnalysisResult> {
    console.log('开始处理文本...');

    const result: AnalysisResult = {
      inputText: text,
      deepseekAnalysis: undefined,
      visualizationSuggestions: undefined,
    };

    try {
      console.log('1. 调用DeepSeek API进行深度分析...');
      const deepseekData = await this.deepseekClient.extractDataFromText(text);
      result.deepseekAnalysis = deepseekData;

      console.log('2. 生成可视化建议...');
      const vizSuggestions = await this.deepseekClient.generateVisualizationSuggestions(deepseekData);
      result.visualizationSuggestions = vizSuggestions;
    } catch (error) {
      console.error('DeepSeek API调用失败:', error);
      result.deepseekError = error instanceof Error ? error.message : String(error);
    }

    // 保存结果
    console.log('3. 保存分析结果...');
    await this.saveResults(result);

    return result;
  }

  /**
   * 处理文件中的文本
   * @param filePath 文件路径
   * @returns 处理结果
   */
  async processFile(filePath: string): Promise<AnalysisResult> {
    try {
      const text = fs.readFileSync(filePath, 'utf-8');
      console.log(`成功读取文件: ${filePath}`);
      return await this.processText(text);
    } catch (error) {
      console.error('文件读取失败:', error);
      return {
        inputText: '',
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  /**
   * 保存分析结果
   * @param result 分析结果
   */
  private async saveResults(result: AnalysisResult): Promise<void> {
    try {
      // 确保输出目录存在
      if (!fs.existsSync(this.outputDir)) {
        fs.mkdirSync(this.outputDir, { recursive: true });
      }

      // 保存JSON结果
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19).replace('T', '_');
      const jsonFilename = `analysis_result_${timestamp}.json`;
      const jsonFilepath = path.join(this.outputDir, jsonFilename);

      fs.writeFileSync(jsonFilepath, JSON.stringify(result, null, 2), 'utf-8');

      console.log(`分析结果已保存到: ${jsonFilepath}`);
    } catch (error) {
      console.error('保存结果失败:', error);
    }
  }

  /**
   * 打印分析摘要
   * @param result 分析结果
   */
  printSummary(result: AnalysisResult): void {
    // TODO: 实现摘要打印逻辑
    console.log('分析摘要功能待实现');
    console.log(`输入文本长度: ${result.inputText.length} 字符`);
    if (result.deepseekAnalysis) {
      console.log('DeepSeek 分析完成');
    }
    if (result.deepseekError) {
      console.log(`DeepSeek 错误: ${result.deepseekError}`);
    }
  }
}
