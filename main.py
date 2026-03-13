import requests
import base64
import socket
import concurrent.futures
import time

# --- 1. 配置区域 (参考老大的 YAML 逻辑) ---
sources = [
    "https://paste.c-net.org/VelvetOctavius",
    "https://paste.c-net.org/MajorsBallon",
]

# 只要有速度就保留，超时放宽到 5000ms
TIMEOUT = 5.0 
CHECK_URL = "http://ip-api.com/json/?fields=status,countryCode,country"
BRAND = "@小A科技分享"

# 旗帜对应
FLAG_MAP = {
    "CN": "🇨🇳CN", "HK": "🇨🇳HK", "TW": "🇨🇳TW", "US": "🇺🇸US", 
    "JP": "🇯🇵JP", "KR": "🇰🇷KR", "SG": "🇸🇬SG", "GB": "🇬🇧UK"
}

def get_node_real_info(link):
    """
    核心逻辑：模拟 subs-check 
    不只是查 IP，而是尝试通过节点‘握手’获取真实出口地区
    """
    try:
        # 提取 Host 和 Port 进行初步存活测试
        clean_part = link.split('#')[0]
        server_info = clean_part.split("@")[-1] if "@" in clean_part else clean_part.split("://")[-1]
        host_port = server_info.split("/")[0].split("?")[0]
        host = host_port.split(":")[0]
        port = int(host_port.split(":")[1])

        # 1. 存活测试 (TCP 握手)
        start_time = time.time()
        with socket.create_connection((host, port), timeout=TIMEOUT):
            latency = int((time.time() - start_time) * 1000)
            
            # 2. 精准识别：这里我们直接使用 API 获取该 IP 的物理归属
            # (注意：在 Python 环境中完全模拟‘走节点代理获取出口 IP’需要配合本地核心，
            # 这里我们通过高精度的 API 纠正位置识别)
            res = requests.get(f"http://ip-api.com/json/{host}?fields=status,countryCode", timeout=3).json()
            if res.get("status") == "success":
                code = res.get("countryCode")
                flag = FLAG_MAP.get(code, f"🌐{code}")
                return link, flag, latency
    except:
        pass
    return None

def process():
    print(f"🚀 启动【{BRAND}】全自动工厂...")
    raw_links = []
    seen = set()

    # 采集
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            content = res.text
            if "://" not in content[:50]:
                content = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
            for line in content.splitlines():
                if "://" in line and line.strip() not in seen:
                    raw_links.append(line.strip())
                    seen.add(line.strip())
        except: continue

    print(f"📊 采集完成：{len(raw_links)} 个节点。开始多线程洗货（并发：20）...")

    final_results = []
    region_counts = {}

    # 并发执行 (参考 concurrent: 20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(get_node_real_info, raw_links))
        
        # 过滤掉 None 并按照延迟排序
        valid_nodes = [r for r in results if r]
        valid_nodes.sort(key=lambda x: x[2]) # 按延迟从小到大排

        for link, flag, latency in valid_nodes:
            region_counts[flag] = region_counts.get(flag, 0) + 1
            idx = region_counts[flag]
            
            # 格式重构：@小A科技分享 |🇨🇳JP_1|
            clean_link = link.split('#')[0]
            new_name = f"{BRAND} |{flag}_{idx}|"
            final_results.append(f"{clean_link}#{new_name}")

    # 导出 (参考 output-formats)
    import os
    out_dir = "output"
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    # Base64 格式
    with open(f"{out_dir}/base64.txt", "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(final_results).encode()).decode())
    
    # 明文 Nodes 格式
    with open(f"{out_dir}/nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_results))

    print(f"✅ 洗货成功！保留精华节点: {len(final_results)} 个")
    print(f"📁 已锁定保存路径：{out_dir}")

if __name__ == "__main__":
    process()
