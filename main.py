import requests
import base64
import socket
import concurrent.futures
import re

# --- 老大的核心源 ---
sources = [
    "https://paste.c-net.org/VelvetOctavius",
    "https://paste.c-net.org/MajorsBallon",
]

# 国旗对应表
FLAG_MAP = {
    "China": "🇨🇳HK", "Hong Kong": "🇨🇳HK", "Taiwan": "🇨🇳TW",
    "United States": "🇺🇸US", "Japan": "🇯🇵JP", "Korea": "🇰🇷KR",
    "Singapore": "🇸🇬SG", "United Kingdom": "🇬🇧UK", "Germany": "🇩🇪DE"
}

def get_region(host):
    """查询 IP 归属地并返回旗帜和缩写"""
    try:
        # 如果是域名先转成 IP
        ip = socket.gethostbyname(host)
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=2).json()
        country = res.get("country", "UN")
        return FLAG_MAP.get(country, f"🌐{country[:2].upper()}")
    except:
        return "🌐UN"

def check_and_format(link):
    """测速 + 格式化名称"""
    try:
        # 解析 host
        clean_part = link.split('#')[0]
        server_info = clean_part.split("@")[-1] if "@" in clean_part else clean_part.split("://")[-1]
        host_port = server_info.split("/")[0].split("?")[0]
        host = host_port.split(":")[0]
        port = int(host_port.split(":")[1])

        # 1. 测速 (TCP 握手)
        with socket.create_connection((host, port), timeout=3):
            # 2. 只有通了的节点才查询地理位置
            region_label = get_region(host)
            return link, region_label
    except:
        return None

def process():
    raw_links = []
    seen = set()
    
    print("📡 正在采集源...")
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

    print(f"🔍 采集到 {len(raw_links)} 个节点，开始洗货并标注地区...")

    final_list = []
    region_counts = {} # 用于生成编号，如 HK_1, HK_2

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(check_and_format, raw_links))
        
        for res in results:
            if res:
                link, region = res[0], res[1]
                # 统计编号
                region_counts[region] = region_counts.get(region, 0) + 1
                index = region_counts[region]
                
                # 3. 构造图二格式：@小A科技分享 |🇨🇳HK_1|
                clean_link = link.split('#')[0]
                formatted_name = f"@小A科技分享 |{region}_{index}|"
                final_list.append(f"{clean_link}#{formatted_name}")

    # 4. 写入文件
    import os
    if not os.path.exists("output"): os.makedirs("output")
    
    with open("output/nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    with open("output/base64.txt", "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(final_list).encode()).decode())

    print(f"✅ 完成！输出精华节点 {len(final_list)} 个，格式已同步图二。")

if __name__ == "__main__":
    process()
