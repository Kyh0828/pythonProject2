import os
import json
import time
import http.client
import urllib.parse
import subprocess
import sys

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
        # 处理路径，确保正确的路径格式
        directory = directory.replace('/', '\\') if '\\' not in directory else directory
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
        # 处理路径，确保正确的路径格式
        old_path = old_path.replace('/', '\\') if '\\' not in old_path else old_path
        directory = os.path.dirname(old_path)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        return f"文件已重命名为：{new_path}"
    except Exception as e:
        return f"错误：{str(e)}"

def delete_file(file_path):
    """删除文件"""
    try:
        # 处理路径，确保正确的路径格式
        file_path = file_path.replace('/', '\\') if '\\' not in file_path else file_path
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
        # 处理路径，确保正确的路径格式
        file_path = file_path.replace('/', '\\') if '\\' not in file_path else file_path
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
        # 处理路径，确保正确的路径格式
        file_path = file_path.replace('/', '\\') if '\\' not in file_path else file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"文件内容：\n{content}"
    except Exception as e:
        return f"错误：{str(e)}"

def curl(url):
    """通过curl访问网页并返回网页内容"""
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or '/'
        if parsed_url.query:
            path += '?' + parsed_url.query
        
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
        
        max_length = 2000
        if len(content) > max_length:
            content = content[:max_length] + "\n... (内容过长，已截断)"
        
        return f"网页内容：\n{content}"
    except Exception as e:
        return f"错误：{str(e)}"

def append_to_chat_log(log_path, records):
    """追加记录到聊天日志文件"""
    try:
        directory = os.path.dirname(log_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(log_path, 'a', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return f"已成功追加 {len(records)} 条记录到 {log_path}"
    except Exception as e:
        return f"错误：{str(e)}"

def read_chat_log(log_path):
    """读取聊天日志文件内容"""
    try:
        if not os.path.exists(log_path):
            return "聊天日志文件不存在"
        
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return "聊天日志文件为空"
        
        return f"聊天日志内容：\n{content}"
    except Exception as e:
        return f"错误：{str(e)}"

def anythingllm_query(message, api_key, workspace_slug):
    """使用subprocess调用curl访问AnythingLLM API"""
    try:
        url = f"http://localhost:3001/api/v1/workspace/ai/chat"
        
        data = {
            "message": message,
            "mode": "chat"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        if sys.platform == 'win32':
            curl_cmd = [
                'curl', '-X', 'POST',
                url,
                '-H', f'Content-Type: application/json',
                '-H', f'Authorization: Bearer {api_key}',
                '-d', json.dumps(data, ensure_ascii=False),
                '--silent'
            ]
        else:
            curl_cmd = [
                'curl', '-X', 'POST',
                url,
                '-H', f'Content-Type: application/json',
                '-H', f'Authorization: Bearer {api_key}',
                '-d', json.dumps(data, ensure_ascii=False),
                '--silent'
            ]
        
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode != 0:
            return f"错误：curl命令执行失败，返回码：{result.returncode}\n错误信息：{result.stderr}"
        
        try:
            response_data = json.loads(result.stdout)
            
            if 'textResponse' in response_data:
                return f"AnythingLLM回复：\n{response_data['textResponse']}"
            elif 'error' in response_data:
                return f"错误：{response_data['error']}"
            else:
                return f"AnythingLLM响应：{result.stdout}"
                
        except json.JSONDecodeError:
            return f"无法解析JSON响应：{result.stdout}"
            
    except Exception as e:
        return f"错误：{str(e)}"

def send_message(base_url, model, api_key, messages):
    """发送消息到LLM服务并返回响应"""
    if base_url.startswith('https://'):
        url = base_url[8:]
        use_https = True
    else:
        url = base_url[7:]
        use_https = False
    
    if '/' in url:
        host, path = url.split('/', 1)
        path = '/' + path
    else:
        host = url
        path = '/'
    
    if not path.endswith('/chat/completions'):
        if path.endswith('/'):
            path += 'chat/completions'
        else:
            path += '/chat/completions'
    
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

def extract_key_info(conversation_history, base_url, model, api_key):
    """调用LLM提取关键信息（5W规则）"""
    extraction_prompt = """
请从以下对话历史中提取关键信息，按照5W规则提取：
- Who（谁）：谁做了这件事
- What（做了什么事）：具体做了什么
- When（什么时候，可选）：事件发生的时间
- Where（在何处，可选）：事件发生的地点
- Why（为什么，可选）：做这件事的原因

请以JSON格式返回，格式如下：
{"who": "人物或主体", "what": "做的事情", "when": "时间（可选）", "where": "地点（可选）", "why": "原因（可选）"}

如果有多条关键信息，请返回JSON数组格式。

对话历史：
"""
    
    dialog_content = ""
    for msg in conversation_history:
        if msg['role'] == 'user':
            dialog_content += f"用户: {msg['content']}\n"
        elif msg['role'] == 'assistant':
            dialog_content += f"助手: {msg['content']}\n"
    
    extraction_messages = [
        {'role': 'system', 'content': '你是一个关键信息提取助手，负责从对话中提取5W关键信息。'},
        {'role': 'user', 'content': extraction_prompt + dialog_content}
    ]
    
    result = send_message(base_url, model, api_key, extraction_messages)
    
    if 'error' not in result:
        try:
            extracted_data = json.loads(result['content'])
            return extracted_data
        except json.JSONDecodeError:
            return result['content']
    return None

def main():
    """主函数：交互式对话循环"""
    env_vars = load_env()
    
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', 'your-api-key-here')
    
    anythingllm_api_key = env_vars.get('ANYTHINGLLM_API_KEY', '')
    anythingllm_workspace_slug = env_vars.get('ANYTHINGLLM_WORKSPACE_SLUG', '')
    
    chat_log_path = r"D:\chat-log\log.txt"
    chat_count = 0
    recent_user_messages = []
    
    if not env_vars:
        print("Warning: .env file not found or empty")
        print("Using default configuration. Please copy env.example to .env and fill in the correct values for production use")
        print()
    
    print("=" * 50)
    print("AI智能体交互系统（工具调用增强版+AnythingLLM）")
    print("输入 'exit' 或按 Ctrl+C 退出")
    print("=" * 50)
    print()
    
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

7. search_chat_history(user_query): 当用户发送的信息用"/search"开头，或用户表达了"查找聊天历史"这个意思，或你认为应该查找聊天历史时使用
   参数：user_query - 用户的查询请求

8. append_to_chat_log(records): 追加记录到聊天日志文件
   参数：records - 要追加的记录列表，格式为JSON数组

9. anythingllm_query(message): 当用户提到"文档仓库"、"文件仓库"、"仓库"时，使用此工具查询AnythingLLM文档仓库
   参数：message - 要查询的内容

使用工具的格式：
调用工具时，请使用以下JSON格式：
{"toolcall": {"name": "工具名称", "params": {"参数1": "值1", "参数2": "值2"}}}

例如：
{"toolcall": {"name": "list_directory", "params": {"directory": "d:\\example"}}}

当你收到工具执行结果后，请用自然语言总结给用户。
"""
    
    conversation_history = [{'role': 'system', 'content': system_prompt}]
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'exit':
                print("\n感谢使用，再见！")
                break
            
            if not user_input:
                continue
            
            search_keywords = ['查找聊天历史', '搜索历史', '查看历史', '历史记录', '以前聊过', '之前说过']
            need_search_history = (
                user_input.startswith('/search') or
                any(keyword in user_input for keyword in search_keywords)
            )
            
            if need_search_history:
                log_content = read_chat_log(chat_log_path)
                
                search_query = user_input.replace('/search', '').strip()
                search_prompt = f"以下是用户的聊天历史记录：\n{log_content}\n\n用户当前请求：{search_query}\n\n请根据聊天历史记录回答用户的当前请求。"
                
                temp_history = conversation_history.copy()
                
                search_messages = [
                    {'role': 'system', 'content': '你是一个智能助手，擅长根据历史聊天记录回答用户的问题。'},
                    {'role': 'user', 'content': search_prompt}
                ]
                
                result = send_message(base_url, model, api_key, search_messages)
                
                if 'error' in result:
                    print(f"Error: {result['error']}")
                    continue
                
                print(f"AI: {result['content']}")
                
                conversation_history = temp_history
                conversation_history.append({'role': 'user', 'content': user_input})
                conversation_history.append({'role': 'assistant', 'content': result['content']})
                
                print(f"[统计] 时间: {result['time_taken']:.2f}s | "
                      f"Token: {result['total_tokens']} | "
                      f"速度: {result['tokens_per_second']:.2f}t/s")
                print()
                continue
            
            chat_count += 1
            recent_user_messages.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                'content': user_input
            })
            
            conversation_history.append({'role': 'user', 'content': user_input})
            
            result = send_message(base_url, model, api_key, conversation_history)
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                conversation_history.pop()
                continue
            
            print(f"AI: {result['content']}")
            
            recent_user_messages.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                'content': user_input,
                'assistant': result['content']
            })
            
            try:
                toolcall_data = json.loads(result['content'])
                if 'toolcall' in toolcall_data:
                    tool_name = toolcall_data['toolcall']['name']
                    tool_params = toolcall_data['toolcall']['params']
                    
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
                    elif tool_name == 'search_chat_history':
                        tool_result = read_chat_log(chat_log_path)
                    elif tool_name == 'append_to_chat_log':
                        tool_result = append_to_chat_log(chat_log_path, tool_params['records'])
                    elif tool_name == 'anythingllm_query':
                        tool_result = anythingllm_query(
                            tool_params['message'],
                            anythingllm_api_key,
                            anythingllm_workspace_slug
                        )
                    else:
                        tool_result = f"错误：未知工具 {tool_name}"
                    
                    print(f"工具执行结果: {tool_result}")
                    
                    conversation_history.append({'role': 'assistant', 'content': result['content']})
                    conversation_history.append({'role': 'user', 'content': f"工具执行结果: {tool_result}"})
                    
                    result = send_message(base_url, model, api_key, conversation_history)
                    if 'error' not in result:
                        print(f"AI: {result['content']}")
                        conversation_history.append({'role': 'assistant', 'content': result['content']})
                else:
                    conversation_history.append({'role': 'assistant', 'content': result['content']})
            except json.JSONDecodeError:
                conversation_history.append({'role': 'assistant', 'content': result['content']})
            except Exception as e:
                print(f"工具调用解析错误: {str(e)}")
                conversation_history.append({'role': 'assistant', 'content': result['content']})
            
            if chat_count >= 5 and chat_count % 5 == 0:
                print("\n[系统] 正在提取聊天关键信息...")
                extracted_info = extract_key_info(conversation_history, base_url, model, api_key)
                
                if extracted_info:
                    print(f"[系统] 提取的关键信息: {extracted_info}")
                    
                    log_records = []
                    if isinstance(extracted_info, list):
                        for info in extracted_info:
                            log_records.append({
                                'type': 'key_info',
                                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                                'info': info
                            })
                    else:
                        log_records.append({
                            'type': 'key_info',
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                            'info': extracted_info
                        })
                    
                    append_result = append_to_chat_log(chat_log_path, log_records)
                    print(f"[系统] {append_result}")
                
                recent_user_messages = []
            
            print(f"[统计] 时间: {result['time_taken']:.2f}s | "
                  f"Token: {result['total_tokens']} | "
                  f"速度: {result['tokens_per_second']:.2f}t/s")
            print()
            
    except KeyboardInterrupt:
        print("\n\n检测到Ctrl+C，程序已退出")
        print("感谢使用，再见！")

if __name__ == "__main__":
    main()
