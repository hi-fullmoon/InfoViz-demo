/**
 * 项目类型定义
 */

export interface DeepSeekResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

export interface DataPoint {
  dataPoint: string;
  relationType: string;
  timeNode?: string;
  informationMeaning: string;
  dataFeature?: string;
  changeAmount?: string;
  duration?: string;
  monthlyIncrease?: string;
  remark?: string;
}

export interface TimeSeriesData {
  month: string;
  changeAmount: string;
}

export interface GoldHoldingCycle {
  cycle: string;
  duration: string;
  endTime?: string;
  timePeriod?: string;
  startTime?: string;
}

export interface MarketReferenceData {
  dataPoint: string;
  relationType: string;
  timeNode: string;
  informationMeaning: string;
  remark?: string;
}

export interface ExtractedData {
  数据提取报告: {
    外汇储备数据: DataPoint[];
    黄金储备数据: DataPoint[];
    占比关系数据: DataPoint[];
    时间序列数据: {
      外汇储备月度变化: TimeSeriesData[];
      黄金增持周期: GoldHoldingCycle[];
    };
    市场参考数据: MarketReferenceData[];
    数据发布日期: string;
    数据来源机构: string[];
  };
}

export interface VisualizationSuggestion {
  type: string;
  title: string;
  description: string;
  data: any;
}

export interface AnalysisResult {
  inputText: string;
  deepseekAnalysis?: ExtractedData;
  visualizationSuggestions?: VisualizationSuggestion[];
  deepseekError?: string;
  error?: string;
}

export interface DeepSeekClientConfig {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
}

export interface InfoVizDemoConfig {
  apiKey?: string;
  outputDir?: string;
}
