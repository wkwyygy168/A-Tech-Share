import requests
import base64
import socket
import concurrent.futures
from urllib.parse import urlparse

# --- 老大的核心源列表 ---
sources = [
    "https://paste.c-net.org/VelvetOctavius",
    "https://paste.c-net.org/MajorsBallon",
]

def check_node_alive(link):
    """
    核心测速逻辑：尝试解析节点地址并进行 TCP 握手。
    如果 TCP 握手失败，说明节点已挂，直接剔除。
    """
    try:
        # 1. 简单的协议提取 (支持 vmess, vless, ss, ssr, trojan, hysteria2 等)
        # 去掉混淆和别名部分，只拿服务器地址和端口
        clean_part = link.split('#')[0]
        if "@" in clean_part:
            server_info = clean_part.split("@")[-1] # 拿 user@host:port 后面这段
        else:
            server_info = clean_part.split("://")[-1]
            
        host_port = server_info.split("/")[0].split("?")[0]
        
        if ":" in host_port:
            host = host_port.split(":")[0]
            port = int(host_port.split(":")[1])
            
            # 2. TCP 握手测试 (超时设为 3 秒，保证质量)
            with socket.create_connection((host, port), timeout=3):
                return link
    except:
        pass
    return None

def process():
    raw_links = []
    seen = set()
    
    print("📡 正在从源采集原始数据...")
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            content = res.text
            # 自动处理 Base64
            if "://" not in content[:50]:
                try:
                    content = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
                except: pass
            
            for line in content.splitlines():
                line = line.strip()
                if "://" in line and line not in seen:
                    raw_links.append(line)
                    seen.add(line)
        except Exception as e:
            print(f"❌ 读取源 {url} 失败: {e}")

    print(f"🔍 采集完成，共 {len(raw_links)} 条。开始深度洗货（多线程测速）...")

    # --- 核心改进：多线程并发洗货 ---
    valid_links = []
    # 开启 50 个线程同步测速，既快又准
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_link = {executor.submit(check_node_alive, link): link for link in raw_links}
        for future in concurrent.futures.as_completed(future_to_link):
            result = future.result()
            if result:
                # 3. 重命名逻辑：@小A科技分享
                clean_link = result.split('#')[0]
                new_link = f"{clean_link}#%20@%E5%B0%8FA%E7%A7%91%E6%8A%80%E5%88%86%E4%BA%AB%20|"
                valid_links.append(new_link)

    # 4. 写入 output 文件夹
    import os
    if not os.path.exists("output"):
        os.makedirs("output")
        
    # 保存原始明文版
    with open("output/nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(valid_links))
        
    # 保存订阅版 (Base64)
    with open("output/base64.txt", "w", encoding="utf-8") as f:
        combined = "\n".join(valid_links)
        f.write(base64.b64encode(combined.encode()).decode())

    print("-" * 30)
    print(f"✅ 洗货完成！")
    print(f"📊 原始节点: {len(raw_links)} 个")
    print(f"🚀 精华节点: {len(valid_links)} 个 (已剔除超时和死链接)")
    print(f"📂 结果已保存至 output 文件夹")

if __name__ == "__main__":
    process()
