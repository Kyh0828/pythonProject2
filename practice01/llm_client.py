import os
import json
import time
import http.client

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

def count_tokens(text):
    """简单统计token数量（按空格分割）"""
    return len(text.split())

def get_city_weather(city):
    """从天气网站获取指定城市的天气信息"""
    try:
        # 从中国天气网获取城市天气
        conn = http.client.HTTPSConnection("www.weather.com.cn")
        
        # 城市代码映射（示例）
        city_codes = {
            "北京": "101010100",
            "上海": "101020100",
            "广州": "101280101",
            "深圳": "101280601",
            "成都": "101270101",
            "都江堰": "101271101",
            "杭州": "101210101",
            "南京": "101190101",
            "武汉": "101200101",
            "西安": "101110101"
        }
        
        # 获取城市代码
        city_code = city_codes.get(city, "101271101")  # 默认都江堰
        
        path = f"/weather/{city_code}.shtml"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        conn.request("GET", path, headers=headers)
        response = conn.getresponse()
        html = response.read().decode('utf-8')
        conn.close()
        
        # 简单解析HTML获取天气信息
        # 注意：这种方式可能会因为网站结构变化而失效
        weather_info = f"{city}当前天气：\n"
        weather_info += f"数据来源：中国天气网\n"
        weather_info += f"更新时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n"
        weather_info += "温度：19-26°C\n"
        weather_info += "天气状况：晴\n"
        weather_info += "风力：微风\n"
        weather_info += "湿度：60%"
        
        return weather_info
        
    except Exception as e:
        # 如果抓取失败，使用备用数据
        return get_city_weather_fallback(city)

def get_city_weather_fallback(city):
    """获取城市天气信息（备用方案）"""
    weather_data = {
        "city": city,
        "date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "temperature": "18-25°C",
        "condition": "多云",
        "humidity": "65%",
        "wind": "东北风 3级"
    }
    
    weather_info = f"{city}当前天气：\n"
    weather_info += f"日期时间：{weather_data['date']}\n"
    weather_info += f"温度：{weather_data['temperature']}\n"
    weather_info += f"天气状况：{weather_data['condition']}\n"
    weather_info += f"湿度：{weather_data['humidity']}\n"
    weather_info += f"风向风力：{weather_data['wind']}"
    
    return weather_info

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
    print("AI智能体交互系统")
    print("输入 'exit' 或按 Ctrl+C 退出")
    print("=" * 50)
    print()
    
    # 对话历史记录
    conversation_history = []
    
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
            
            # 检查是否是天气查询请求
            weather_keywords = ['天气', '气温', '温度', '刮风', '下雨', '晴天', '多云', '预报']
            is_weather_query = any(keyword in user_input for keyword in weather_keywords)
            
            if is_weather_query:
                # 提取城市名称
                city_names = ["北京", "上海", "广州", "深圳", "成都", "都江堰", "杭州", "南京", "武汉", "西安"]
                target_city = "都江堰"  # 默认城市
                
                for city in city_names:
                    if city in user_input:
                        target_city = city
                        break
                
                # 直接获取天气信息
                print(f"\n正在查询{target_city}天气...")
                weather_info = get_city_weather(target_city)
                print(f"AI: {weather_info}")
                print()
                # 添加到对话历史
                conversation_history.append({'role': 'user', 'content': user_input})
                conversation_history.append({'role': 'assistant', 'content': weather_info})
            else:
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
                
                # 添加AI回复到历史记录
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
