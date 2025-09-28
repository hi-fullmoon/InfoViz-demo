#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * 增强版生成 demo.html 文件的脚本
 * 从 visualization_result.json 读取数据，替换 demo_template.html 中的变量
 * 包含更详细的错误处理和日志输出
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

    console.log('📖 读取 visualization_result.json...');
    const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

    console.log('📖 读取 demo_template.html...');
    let templateContent = fs.readFileSync(templatePath, 'utf8');

    // 检查必要的字段
    if (!jsonData.visualization_result) {
      throw new Error('visualization_result.json 中缺少 visualization_result 字段');
    }

    // 解析 visualization_result 字段
    const visualizationResult = JSON.parse(jsonData.visualization_result);

    console.log('🔄 开始替换模板变量...');

    // 替换变量
    const replacements = {
      '{{title}}': '数据可视化分析报告',
      '{{description}}': visualizationResult.description || '基于AI智能分析的数据可视化展示',
      '{{timestamp}}': jsonData.timestamp || new Date().toISOString(),
      '{{charts_json}}': JSON.stringify(visualizationResult),
    };

    // 执行替换
    let replacedCount = 0;
    for (const [placeholder, value] of Object.entries(replacements)) {
      const regex = new RegExp(placeholder.replace(/[{}]/g, '\\$&'), 'g');
      const matches = templateContent.match(regex);
      if (matches) {
        replacedCount += matches.length;
        templateContent = templateContent.replace(regex, value);
        console.log(`  ✓ 替换 ${placeholder} (${matches.length} 次)`);
      }
    }

    console.log(`✅ 成功替换了 ${replacedCount} 个变量`);

    console.log('💾 写入 demo.html 文件...');
    fs.writeFileSync(outputPath, templateContent, 'utf8');

    console.log('✅ demo.html 文件生成成功！');
    console.log(`📁 输出文件: ${outputPath}`);

    // 显示一些统计信息
    const chartCount = visualizationResult.charts ? visualizationResult.charts.length : 0;
    console.log(`📊 包含 ${chartCount} 个图表`);

    // 显示文件大小
    const stats = fs.statSync(outputPath);
    const fileSizeKB = (stats.size / 1024).toFixed(2);
    console.log(`📏 文件大小: ${fileSizeKB} KB`);

    // 显示图表详情
    if (chartCount > 0) {
      console.log('📈 图表列表:');
      visualizationResult.charts.forEach((chart, index) => {
        console.log(`  ${index + 1}. ${chart.title} (${chart.type})`);
      });
    }
  } catch (error) {
    console.error('❌ 生成过程中出现错误:', error.message);
    console.error('💡 请确保以下文件存在:');
    console.error('   - visualization_result.json');
    console.error('   - demo_template.html');
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  generateDemo();
}

module.exports = { generateDemo };
