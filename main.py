import requests, base64, socket, concurrent.futures, time

sources = ["https://paste.c-net.org/VelvetOctavius", "https://paste.c-net.org/MajorsBallon"]
FLAG_MAP = {"CN": "🇨🇳CN", "HK": "🇨🇳HK", "TW": "🇨🇳TW", "US": "🇺🇸US", "JP": "🇯🇵JP", "KR": "🇰🇷KR", "SG": "🇸🇬SG"}

def check_node(link):
    try:
        clean_link = link.split('#')[0]
        server = clean_link.split("@")[-1] if "@" in clean_link else clean_link.split("://")[-1]
        host = server.split("/")[0].split("?")[0].split(":")[0]
        port = int(server.split("/")[0].split("?")[0].split(":")[1])
        with socket.create_connection((host, port), timeout=3):
            res = requests.get(f"http://ip-api.com/json/{host}?fields=countryCode", timeout=2).json()
            flag = FLAG_MAP.get(res.get("countryCode"), f"🌐{res.get('countryCode')}")
            return f"{clean_link}#@小A科技分享 |{flag}|"
    except: return None

def process():
    all_raw = []
    for url in sources:
        try:
            content = requests.get(url, timeout=10).text
            if "://" not in content[:50]: content = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
            all_raw.extend([l.strip() for l in content.splitlines() if "://" in l])
    all_raw = list(set(all_raw))
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as exe:
        valid = [r for r in list(exe.map(check_node, all_raw)) if r]
    import os
    if not os.path.exists("output"): os.makedirs("output")
    with open("output/nodes.txt", "w", encoding="utf-8") as f: f.write("\n".join(valid))
    with open("output/base64.txt", "w", encoding="utf-8") as f: f.write(base64.b64encode("\n".join(valid).encode()).decode())

if __name__ == "__main__":
    process()
