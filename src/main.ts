/**
 * 主程序入口
 * 整合DeepSeek API调用、文本处理和数据可视化功能
 */

import { Command } from 'commander';
import { InfoVizDemo } from './infoviz-demo';

/**
 * 主函数
 */
async function main() {
  const program = new Command();

  program.name('infoviz-demo').description('信息可视化演示程序').version('1.0.0');

  program
    .option('-t, --text <text>', '要分析的文本内容')
    .option('-f, --file <file>', '要分析的文件路径')
    .option('-k, --api-key <key>', 'DeepSeek API密钥')
    .option('-o, --output-dir <dir>', '输出目录', 'output');

  program.parse();

  const options = program.opts();

  // 检查输入
  if (!options.text && !options.file) {
    console.error('错误: 请提供要分析的文本 (--text) 或文件路径 (--file)');
    process.exit(1);
  }

  // 初始化程序
  let app: InfoVizDemo;
  try {
    app = new InfoVizDemo({
      apiKey: options.apiKey,
      outputDir: options.outputDir,
    });
  } catch (error) {
    console.error('初始化失败:', error);
    process.exit(1);
  }

  try {
    // 处理文本
    let result;
    if (options.text) {
      result = await app.processText(options.text);
    } else if (options.file) {
      result = await app.processFile(options.file);
    } else {
      console.error('错误: 请提供要分析的文本或文件路径');
      process.exit(1);
    }

    // 打印摘要
    app.printSummary(result);

    console.log(`\n分析完成! 结果已保存到 ${options.outputDir} 目录`);
  } catch (error) {
    console.error('处理过程中发生错误:', error);
    process.exit(1);
  }
}

// 如果直接运行此文件，则执行主函数
if (require.main === module) {
  main().catch((error) => {
    console.error('程序执行失败:', error);
    process.exit(1);
  });
}
