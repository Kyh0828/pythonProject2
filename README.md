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
├── practice02/          # 第二次实践代码
│   └── tool_chat_client.py  # 工具调用版LLM客户端程序
├── practice03/          # 第三次实践代码
│   └── tool_chat_client.py  # 工具调用增强版（包含聊天日志和5W提取）
└── practice04/          # 第四次实践代码
    └── tool_chat_client.py  # 工具调用增强版+AnythingLLM集成
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

### practice03/tool_chat_client.py
**功能用途**：
- 基于practice02的所有功能
- **新增功能（1）**：主动触发LLM，每5次聊天提取一次关键信息
  - 按照5W规则提取：Who、What、When（可选）、Where（可选）、Why（可选）
  - 自动记录到用户本地 D:\chat-log\log.txt
  - 支持目录和文件自动创建
  - 日志文件进行增量更新
- **新增功能（2）**：聊天历史搜索function call
  - 当用户发送的信息以"/search"开头时触发
  - 或用户表达"查找聊天历史"等意思时触发
  - 或LLM认为应该查找聊天历史时触发
  - 将log.txt内容和用户请求结合发送给LLM
  - 完成完整的LLM请求并得到回复

**新增工具**：
- `search_chat_history(user_query)`: 搜索聊天历史记录
- `append_to_chat_log(records)`: 追加记录到聊天日志文件

**日志格式**：
日志文件位于 D:\chat-log\log.txt，每条记录为JSON格式，包含：
- type: 记录类型
- timestamp: 时间戳
- info: 提取的关键信息（包含who、what、when、where、why字段）

**实现的教学目标**：
1. 掌握周期性任务触发机制
2. 学习结构化信息提取（5W规则）
3. 理解增量日志管理
4. 实现基于条件的动态function call触发
5. 学习聊天历史检索和上下文结合

### practice04/tool_chat_client.py
**功能用途**：
- 基于practice03的所有功能
- **新增功能**：AnythingLLM文档仓库查询集成
  - 使用subprocess模块调用curl命令访问AnythingLLM API
  - 访问 `http://localhost:3001/api/v1/workspace/{workspace_slug}/chat` 接口
  - 通过message字段发送查询内容
  - 使用API密钥进行认证
  - 正确处理中文编码问题
  - 从.env文件读取ANYTHINGLLM_API_KEY和ANYTHINGLLM_WORKSPACE_SLUG变量
  - 当用户提到"文档仓库"、"文件仓库"、"仓库"时触发查询

**新增工具**：
- `anythingllm_query(message)`: 查询AnythingLLM文档仓库
  - 参数：message - 要查询的内容
  - 自动从环境变量读取API密钥和工作空间标识符

**环境变量配置**：
在.env文件中添加以下配置：
- ANYTHINGLLM_API_KEY: AnythingLLM的API密钥
- ANYTHINGLLM_WORKSPACE_SLUG: AnythingLLM的工作空间标识符

**实现的教学目标**：
1. 学习subprocess模块的使用
2. 掌握curl命令的编程调用
3. 理解第三方API集成方法
4. 学习中文编码处理
5. 掌握API认证机制
6. 实现基于关键词的工具触发机制

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

### practice03/tool_chat_client.py
1. 配置.env文件（与practice01相同）
2. 运行命令：`python practice03/tool_chat_client.py`
3. 基础功能同practice02
4. **新增功能**：
   - 聊天历史搜索：输入"/search 关键词"或直接说"查找聊天历史"
   - 关键信息提取：每5次聊天自动提取5W关键信息并存入日志
   - 日志文件位置：D:\chat-log\log.txt（自动创建）
5. 示例：
   - "/search Python" - 搜索聊天历史中关于Python的内容
   - "查找聊天历史" - 查看之前的所有聊天记录

### practice04/tool_chat_client.py
1. 配置.env文件：
   - 复制.env.example到.env
   - 填写OpenAI兼容API配置（BASE_URL、MODEL、API_KEY）
   - 填写AnythingLLM配置（ANYTHINGLLM_API_KEY、ANYTHINGLLM_WORKSPACE_SLUG）
2. 确保AnythingLLM服务运行在 http://localhost:3001
3. 运行命令：`python practice04/tool_chat_client.py`
4. 基础功能同practice03
5. **新增功能**：
   - 文档仓库查询：提到"文档仓库"、"文件仓库"、"仓库"时自动查询AnythingLLM
   - 示例：
     - "查询文档仓库中关于Python的内容"
     - "在文件仓库中搜索API文档"
     - "仓库里有关于机器学习的文档吗？"

## 配置说明
在.env文件中配置以下参数：
- BASE_URL: LLM服务的基础URL
- MODEL: 使用的模型名称
- API_KEY: API访问密钥
- ANYTHINGLLM_API_KEY: AnythingLLM的API密钥（practice04需要）
- ANYTHINGLLM_WORKSPACE_SLUG: AnythingLLM的工作空间标识符（practice04需要）

## 更新日志
- 第一次课：创建基础项目结构，实现单次LLM交互
- 第四次课01节：升级为交互式对话系统，支持多轮对话和历史记录
- 第四次课02节：实现工具调用功能（文件操作、curl网络访问）
- 第五次课01节：
  - 实现每5次聊天自动提取5W关键信息并记录到D:\chat-log\log.txt
  - 新增聊天历史搜索功能（/search命令或关键词触发）
  - 创建practice03目录，实现功能分离
- 第五次课02节：
  - 集成AnythingLLM文档仓库查询功能
  - 使用subprocess模块调用curl访问AnythingLLM API
  - 实现中文编码处理和API认证
  - 新增anythingllm_query工具，支持文档仓库查询
  - 创建practice04目录，添加环境变量配置
