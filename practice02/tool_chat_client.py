import os
import json
import time
import http.client
import urllib.parse

def load_env():
    """加载环境变量配置文件"""
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    return env_vars

def list_directory(directory):
    """列出目录下的文件及其基本属性"""
    try:
        files = os.listdir(directory)
        result = f"目录 {directory} 下的文件：\n"
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                mtime = os.path.getmtime(file_path)
                mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                result += f"- {file} (文件, 大小: {size} 字节, 修改时间: {mtime_str})\n"
            elif os.path.isdir(file_path):
                result += f"- {file} (目录)\n"
        return result
    except Exception as e:
        return f"错误：{str(e)}"

def rename_file(old_path, new_name):
    """修改文件名字"""
    try:
        directory = os.path.dirname(old_path)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        return f"文件已重命名为：{new_path}"
    except Exception as e:
        return f"错误：{str(e)}"

def delete_file(file_path):
    """删除文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"文件已删除：{file_path}"
        else:
            return f"错误：文件不存在"
    except Exception as e:
        return f"错误：{str(e)}"

def create_file(file_path, content):
    """新建文件并写入内容"""
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"文件已创建并写入内容：{file_path}"
    except Exception as e:
        return f"错误：{str(e)}"

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"文件内容：\n{content}"
    except Exception as e:
        return f"错误：{str(e)}"

def curl(url):
    """通过curl访问网页并返回网页内容"""
    try:
        # 解析URL
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or '/'
        if parsed_url.query:
            path += '?' + parsed_url.query
        
        # 创建连接
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(host)
        else:
            conn = http.client.HTTPConnection(host)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        conn.request("GET", path, headers=headers)
        response = conn.getresponse()
        content = response.read().decode('utf-8', errors='replace')
        conn.close()
        
        # 限制返回内容长度
        max_length = 2000
        if len(content) > max_length:
            content = content[:max_length] + "\n... (内容过长，已截断)"
        
        return f"网页内容：\n{content}"
    except Exception as e:
        return f"错误：{str(e)}"

def send_message(base_url, model, api_key, messages):
    """发送消息到LLM服务并返回响应"""
    # 解析URL
    if base_url.startswith('https://'):
        url = base_url[8:]
        use_https = True
    else:
        url = base_url[7:]
        use_https = False
    
    # 分离主机和路径
    if '/' in url:
        host, path = url.split('/', 1)
        path = '/' + path
    else:
        host = url
        path = '/'
    
    # 处理路径
    if not path.endswith('/chat/completions'):
        if path.endswith('/'):
            path += 'chat/completions'
        else:
            path += '/chat/completions'
    
    # 创建连接
    if use_https:
        conn = http.client.HTTPSConnection(host)
    else:
        conn = http.client.HTTPConnection(host)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'model': model,
        'messages': messages
    }
    
    try:
        start_time = time.time()
        conn.request('POST', path, json.dumps(data), headers)
        response = conn.getresponse()
        response_data = json.loads(response.read().decode())
        end_time = time.time()
        
        if 'choices' in response_data:
            completion = response_data['choices'][0]['message']['content']
            prompt_tokens = response_data['usage']['prompt_tokens']
            completion_tokens = response_data['usage']['total_tokens'] - prompt_tokens
            total_tokens = response_data['usage']['total_tokens']
            time_taken = end_time - start_time
            tokens_per_second = total_tokens / time_taken if time_taken > 0 else 0
            
            return {
                'content': completion,
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'time_taken': time_taken,
                'tokens_per_second': tokens_per_second
            }
        else:
            return {'error': response_data.get('error', 'Unknown error')}
            
    except Exception as e:
        return {'error': str(e)}
    finally:
        conn.close()

def main():
    """主函数：交互式对话循环"""
    env_vars = load_env()
    
    # 默认配置
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', 'your-api-key-here')
    
    # 提示用户配置
    if not env_vars:
        print("Warning: .env file not found or empty")
        print("Using default configuration. Please copy env.example to .env and fill in the correct values for production use")
        print()
    
    print("=" * 50)
    print("AI智能体交互系统（工具调用版）")
    print("输入 'exit' 或按 Ctrl+C 退出")
    print("=" * 50)
    print()
    
    # 系统提示词
    system_prompt = """
你是一个智能助手，能够使用以下工具来帮助用户完成任务：

工具列表：
1. list_directory(directory): 列出目录下的文件及其基本属性（大小、修改时间等）
   参数：directory - 要列出的目录路径

2. rename_file(old_path, new_name): 修改文件名字
   参数：old_path - 原文件路径
   参数：new_name - 新文件名

3. delete_file(file_path): 删除文件
   参数：file_path - 要删除的文件路径

4. create_file(file_path, content): 新建文件并写入内容
   参数：file_path - 新文件路径
   参数：content - 要写入的内容

5. read_file(file_path): 读取文件内容
   参数：file_path - 要读取的文件路径

6. curl(url): 通过curl访问网页并返回网页内容
   参数：url - 要访问的网页URL

使用工具的格式：
调用工具时，请使用以下JSON格式：
{"toolcall": {"name": "工具名称", "params": {"参数1": "值1", "参数2": "值2"}}}

例如：
{"toolcall": {"name": "list_directory", "params": {"directory": "d:\\example"}}}

当你收到工具执行结果后，请用自然语言总结给用户。
"""
    
    # 对话历史记录
    conversation_history = [{'role': 'system', 'content': system_prompt}]
    
    try:
        while True:
            # 获取用户输入
            user_input = input("You: ").strip()
            
            # 检查退出命令
            if user_input.lower() == 'exit':
                print("\n感谢使用，再见！")
                break
            
            if not user_input:
                continue
            
            # 添加用户消息到历史记录
            conversation_history.append({'role': 'user', 'content': user_input})
            
            # 发送消息到LLM
            result = send_message(base_url, model, api_key, conversation_history)
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                # 移除失败的用户消息
                conversation_history.pop()
                continue
            
            # 显示AI回复
            print(f"AI: {result['content']}")
            
            # 检查是否需要调用工具
            try:
                # 尝试解析工具调用请求
                toolcall_data = json.loads(result['content'])
                if 'toolcall' in toolcall_data:
                    tool_name = toolcall_data['toolcall']['name']
                    tool_params = toolcall_data['toolcall']['params']
                    
                    # 执行工具
                    tool_result = ""
                    if tool_name == 'list_directory':
                        tool_result = list_directory(tool_params['directory'])
                    elif tool_name == 'rename_file':
                        tool_result = rename_file(tool_params['old_path'], tool_params['new_name'])
                    elif tool_name == 'delete_file':
                        tool_result = delete_file(tool_params['file_path'])
                    elif tool_name == 'create_file':
                        tool_result = create_file(tool_params['file_path'], tool_params['content'])
                    elif tool_name == 'read_file':
                        tool_result = read_file(tool_params['file_path'])
                    elif tool_name == 'curl':
                        tool_result = curl(tool_params['url'])
                    else:
                        tool_result = f"错误：未知工具 {tool_name}"
                    
                    # 显示工具执行结果
                    print(f"工具执行结果: {tool_result}")
                    
                    # 将工具执行结果添加到对话历史
                    conversation_history.append({'role': 'assistant', 'content': result['content']})
                    conversation_history.append({'role': 'user', 'content': f"工具执行结果: {tool_result}"})
                    
                    # 再次发送到LLM以获取总结
                    result = send_message(base_url, model, api_key, conversation_history)
                    if 'error' not in result:
                        print(f"AI: {result['content']}")
                        conversation_history.append({'role': 'assistant', 'content': result['content']})
                else:
                    # 普通回复，直接添加到历史记录
                    conversation_history.append({'role': 'assistant', 'content': result['content']})
            except json.JSONDecodeError:
                # 不是工具调用，普通回复
                conversation_history.append({'role': 'assistant', 'content': result['content']})
            except Exception as e:
                print(f"工具调用解析错误: {str(e)}")
                conversation_history.append({'role': 'assistant', 'content': result['content']})
            
            # 显示统计信息
            print(f"[统计] 时间: {result['time_taken']:.2f}s | "
                  f"Token: {result['total_tokens']} | "
                  f"速度: {result['tokens_per_second']:.2f}t/s")
            print()
            
    except KeyboardInterrupt:
        print("\n\n检测到Ctrl+C，程序已退出")
        print("感谢使用，再见！")

if __name__ == "__main__":
    main()
