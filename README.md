# AI智能体开发教学项目

## 项目概述
本项目是一个基于Python的AI智能体开发教学项目，旨在学习如何与LLM（大语言模型）进行交互。

## 环境配置
- Python 3.6.5
- 使用venv虚拟环境
- 依赖Python标准库（os, json, time, http.client）

## 项目结构
```
pythonProject1/
├── .env                  # LLM配置信息（不提交到git）
├── .env.example          # 配置模板
├── .gitignore           # Git排除文件
├── README.md            # 项目说明文档
├── venv/                # Python虚拟环境
├── practice01/          # 第一次实践代码
│   └── llm_client.py    # LLM客户端程序
└── practice02/          # 第二次实践代码
    └── tool_chat_client.py  # 工具调用版LLM客户端程序
```

## 功能说明

### practice01/llm_client.py
**功能用途**：
- 读取.env文件中的LLM配置信息
- 使用Python标准http库与LLM服务进行通信
- 支持交互式对话循环，可连续输入多个问题
- 维护对话历史记录，实现上下文感知的多轮对话
- 支持用户输入'exit'退出或Ctrl+C中断程序
- 统计token消耗、请求时间和处理速度

**实现的教学目标**：
1. 学习Python环境配置和虚拟环境使用
2. 掌握HTTP客户端编程
3. 理解OpenAI兼容API的调用方式
4. 学习基本的性能监控和统计
5. 实现交互式命令行界面
6. 理解对话上下文管理和历史记录维护

### practice02/tool_chat_client.py
**功能用途**：
- 基于practice01的基础功能
- 实现工具调用能力，包括：
  1. `list_directory(directory)`: 列出目录下的文件及其基本属性
  2. `rename_file(old_path, new_name)`: 修改文件名字
  3. `delete_file(file_path)`: 删除文件
  4. `create_file(file_path, content)`: 新建文件并写入内容
  5. `read_file(file_path)`: 读取文件内容
  6. `curl(url)`: 通过curl访问网页并返回网页内容
- 通过系统提示词指导LLM使用这些工具
- 支持工具调用结果的处理和总结

**实现的教学目标**：
1. 学习工具调用的设计模式
2. 掌握文件系统操作的Python实现
3. 理解网络请求的实现方法
4. 学习如何通过系统提示词指导LLM使用工具
5. 掌握JSON格式的工具调用请求和响应处理

## 使用方法
### practice01/llm_client.py
1. 配置.env文件（复制.env.example并填写正确参数）
2. 运行命令：`python practice01/llm_client.py`
3. 在终端中输入您的问题，AI会回复
4. 可以继续输入下一个问题，AI会记住之前的对话
5. 输入'exit'或按Ctrl+C退出程序

### practice02/tool_chat_client.py
1. 配置.env文件（与practice01相同）
2. 运行命令：`python practice02/tool_chat_client.py`
3. 在终端中输入您的请求，例如：
   - "列出d:\\小学期\\PythonProject2目录下的文件"
   - "在d:\\temp目录下创建一个名为test.txt的文件，内容为'Hello World'"
   - "访问https://www.baidu.com并返回内容"
4. AI会根据系统提示词使用相应的工具来完成任务
5. 输入'exit'或按Ctrl+C退出程序

## 配置说明
在.env文件中配置以下参数：
- BASE_URL: LLM服务的基础URL
- MODEL: 使用的模型名称
- API_KEY: API访问密钥

## 更新日志
- 第一次课：创建基础项目结构，实现单次LLM交互
- 第四次课01节：升级为交互式对话系统，支持多轮对话和历史记录
