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

export interface AnalysisResult {
  inputText: string;
  deepseekAnalysis?: any;
  visualizationSuggestions?: any;
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
