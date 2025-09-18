#!/bin/bash

# InfoViz-demo 启动脚本
# 使用方法: ./run.sh [参数]

# 激活虚拟环境
source .venv/bin/activate

# 运行主程序，传递所有参数
python main.py "$@"
