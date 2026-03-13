import requests
import base64
import socket
import concurrent.futures

# --- 老大的核心源 ---
sources = [
    "https://paste.c-net.org/VelvetOctavius",
    "https://paste.c-net.org/MajorsBallon",
]

# 扩展旗帜库
FLAG_MAP = {
    "CN": "🇨🇳CN", "HK": "🇨🇳HK", "TW": "🇨🇳TW", "MO": "🇨🇳MO",
    "US": "🇺🇸US", "JP": "🇯🇵JP", "KR": "🇰🇷KR", "SG": "🇸🇬SG",
    "GB": "🇬🇧UK", "DE": "🇩🇪DE", "FR": "🇫🇷FR", "RU": "🇷🇺RU",
    "CA": "🇨🇦CA", "AU": "🇦🇺AU", "IN": "🇮🇳IN", "NL": "🇳🇱NL"
}

def get_real_region(host):
    """
    通过可靠的 API 获取准确的国家代码
    """
    try:
        # 1. 尝试将 host 转为 IP
        ip = socket.gethostbyname(host)
        # 2. 使用 ip-api (带 fields 过滤更快)
        api_url = f"http://ip-api.com/json/{ip}?fields=status,countryCode"
        res = requests.get(api_url, timeout=3).json()
        
        if res.get("status") == "success":
            code = res.get("countryCode")
            return FLAG_MAP.get(code, f"🌐{code}")
    except:
        pass
    return "🌐UN"

def check_and_format(link):
    """
    测速 + 精准识别地区
    """
    try:
        # 提取 Host
        clean_part = link.split('#')[0]
        if "@" in clean_part:
            server_info = clean_part.split("@")[-1]
        else:
            server_info = clean_part.split("://")[-1]
            
        host_port = server_info.split("/")[0].split("?")[0]
        
        if ":" in host_port:
            host = host_port.split(":")[0]
            port = int(host_port.split(":")[1])
            
            # 1. 测速（只有通的才查归属地，节省 API 额度）
            with socket.create_connection((host, port), timeout=2.5):
                # 2. 获取准确地区
                region_label = get_real_region(host)
                return link, region_label
    except:
        return None

def process():
    raw_links = []
    seen = set()
    
    print("📡 正在精准采集节点...")
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

    final_list = []
    region_counts = {}

    # 提高线程到 50，快速过一遍
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_and_format, raw_links))
        
        for res in results:
            if res:
                link, region = res[0], res[1]
                region_counts[region] = region_counts.get(region, 0) + 1
                index = region_counts[region]
                
                # 构造图二要求的格式
                clean_link = link.split('#')[0]
                formatted_name = f"@小A科技分享 |{region}_{index}|"
                final_list.append(f"{clean_link}#{formatted_name}")

    # 写入文件
    import os
    if not os.path.exists("output"): os.makedirs("output")
    
    with open("output/nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    with open("output/base64.txt", "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(final_list).encode()).decode())

    print("-" * 30)
    print(f"✅ 精准洗货完成！")
    print(f"📊 获得优质节点: {len(final_list)} 个")
    print(f"🌐 地区分布: { {k: v for k, v in region_counts.items() if v > 0} }")

if __name__ == "__main__":
    process()
