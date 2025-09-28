#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * 生成 demo.html 文件的脚本
 * 从 visualization_result.json 读取数据，替换 demo_template.html 中的变量
 */

function generateDemo() {
  try {
    console.log('🚀 开始生成 demo.html 文件...');

    // 文件路径
    const jsonPath = path.join(__dirname, 'visualization_result.json');
    const templatePath = path.join(__dirname, 'demo_template.html');
    const outputPath = path.join(__dirname, 'demo.html');

    // 检查文件是否存在
    if (!fs.existsSync(jsonPath)) {
      throw new Error(`找不到文件: ${jsonPath}`);
    }
    if (!fs.existsSync(templatePath)) {
      throw new Error(`找不到文件: ${templatePath}`);
    }

    // 读取文件
    const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    let templateContent = fs.readFileSync(templatePath, 'utf8');

    // 检查必要的字段
    if (!jsonData.visualization_result) {
      throw new Error('visualization_result.json 中缺少 visualization_result 字段');
    }

    // 解析 visualization_result 字段
    const visualizationResult = JSON.parse(jsonData.visualization_result);

    // 替换变量
    const replacements = {
      '{{title}}': '数据可视化分析报告',
      '{{description}}': visualizationResult.description || '基于AI智能分析的数据可视化展示',
      '{{timestamp}}': jsonData.timestamp || new Date().toISOString(),
      '{{charts_json}}': JSON.stringify(visualizationResult),
    };

    // 执行替换
    for (const [placeholder, value] of Object.entries(replacements)) {
      const regex = new RegExp(placeholder.replace(/[{}]/g, '\\$&'), 'g');
      templateContent = templateContent.replace(regex, value);
    }

    // 写入文件
    fs.writeFileSync(outputPath, templateContent, 'utf8');

    console.log('✅ demo.html 文件生成成功！');
    console.log(`📁 输出文件: ${outputPath}`);

    // 显示统计信息
    const chartCount = visualizationResult.visualizations ? visualizationResult.visualizations.length : 0;
    console.log(`📊 包含 ${chartCount} 个可视化项`);

  } catch (error) {
    console.error('❌ 生成过程中出现错误:', error.message);
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  generateDemo();
}

module.exports = { generateDemo };
